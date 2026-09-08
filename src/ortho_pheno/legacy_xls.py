"""Minimal read-only BIFF8/CFB reader for the legacy .xls exports in this project.

The project source archive includes six old binary Excel workbooks. This module
implements only the subset needed to recover worksheet names and cell values for
privacy-preserving cohort aggregation. It does not write or modify spreadsheets.
"""

from pathlib import Path
import struct

FREESECT = 0xFFFFFFFF
ENDOFCHAIN = 0xFFFFFFFE


def u16(buf, offset=0):
    return struct.unpack_from("<H", buf, offset)[0]


def u32(buf, offset=0):
    return struct.unpack_from("<I", buf, offset)[0]


def u64(buf, offset=0):
    return struct.unpack_from("<Q", buf, offset)[0]


class CFB:
    def __init__(self, path):
        self.data = Path(path).read_bytes()
        header = self.data[:512]
        if header[:8] != bytes.fromhex("D0CF11E0A1B11AE1"):
            raise ValueError("Not a Compound File Binary document")

        self.sector_size = 1 << u16(header, 30)
        self.mini_sector_size = 1 << u16(header, 32)
        self.num_fat = u32(header, 44)
        self.first_dir = u32(header, 48)
        self.mini_cutoff = u32(header, 56)
        self.first_minifat = u32(header, 60)
        self.num_minifat = u32(header, 64)
        first_difat = u32(header, 68)
        num_difat = u32(header, 72)

        difat = [u32(header, 76 + 4 * i) for i in range(109)]
        sector = first_difat
        for _ in range(num_difat):
            if sector in (FREESECT, ENDOFCHAIN):
                break
            block = self.sector(sector)
            n = self.sector_size // 4
            difat.extend(u32(block, 4 * i) for i in range(n - 1))
            sector = u32(block, 4 * (n - 1))

        fat_sectors = [x for x in difat if x not in (FREESECT, ENDOFCHAIN)][: self.num_fat]
        self.fat = []
        for fat_sector in fat_sectors:
            block = self.sector(fat_sector)
            self.fat.extend(u32(block, 4 * i) for i in range(self.sector_size // 4))

        directory_bytes = self.read_chain(self.first_dir)
        self.directory = []
        for offset in range(0, len(directory_bytes), 128):
            entry = directory_bytes[offset : offset + 128]
            if len(entry) < 128:
                break
            name_len = u16(entry, 64)
            name = entry[: max(0, name_len - 2)].decode("utf-16le", "ignore") if name_len >= 2 else ""
            entry_type = entry[66]
            start_sector = u32(entry, 116)
            size = u64(entry, 120)
            if entry_type:
                self.directory.append((name, entry_type, start_sector, size))

        root = next(entry for entry in self.directory if entry[1] == 5)
        self.ministream = self.read_chain(root[2])[: root[3]]
        self.minifat = []
        if self.num_minifat and self.first_minifat not in (FREESECT, ENDOFCHAIN):
            raw = self.read_chain(self.first_minifat)
            self.minifat = [u32(raw, 4 * i) for i in range(len(raw) // 4)]

    def sector(self, sector_id):
        start = 512 + sector_id * self.sector_size
        return self.data[start : start + self.sector_size]

    def read_chain(self, start_sector):
        out = bytearray()
        sector = start_sector
        seen = set()
        while (
            sector not in (FREESECT, ENDOFCHAIN)
            and sector < len(self.fat)
            and sector not in seen
        ):
            seen.add(sector)
            out.extend(self.sector(sector))
            sector = self.fat[sector]
        return bytes(out)

    def read_stream(self, name):
        entry = next((entry for entry in self.directory if entry[0] == name), None)
        if entry is None:
            return None
        _, _, start_sector, size = entry

        if size < self.mini_cutoff and self.minifat:
            out = bytearray()
            sector = start_sector
            seen = set()
            while (
                sector not in (FREESECT, ENDOFCHAIN)
                and sector < len(self.minifat)
                and sector not in seen
            ):
                seen.add(sector)
                offset = sector * self.mini_sector_size
                out.extend(self.ministream[offset : offset + self.mini_sector_size])
                sector = self.minifat[sector]
            return bytes(out[:size])

        return self.read_chain(start_sector)[:size]


class SegmentCursor:
    def __init__(self, segments):
        self.segments = segments
        self.segment_index = 0
        self.offset = 0

    def _ensure(self):
        while self.segment_index < len(self.segments) and self.offset >= len(self.segments[self.segment_index]):
            self.segment_index += 1
            self.offset = 0
        if self.segment_index >= len(self.segments):
            raise EOFError

    def read(self, nbytes):
        out = bytearray()
        remaining = nbytes
        while remaining:
            self._ensure()
            segment = self.segments[self.segment_index]
            take = min(remaining, len(segment) - self.offset)
            out.extend(segment[self.offset : self.offset + take])
            self.offset += take
            remaining -= take
        return bytes(out)

    def read_u8(self):
        return self.read(1)[0]

    def read_u16(self):
        return u16(self.read(2))

    def read_u32(self):
        return u32(self.read(4))

    def read_chars(self, char_count, high_byte):
        parts = []
        remaining = char_count
        width = 2 if high_byte else 1
        while remaining > 0:
            self._ensure()
            segment = self.segments[self.segment_index]
            available = len(segment) - self.offset
            chars_available = available // width
            if chars_available > 0:
                n_chars = min(remaining, chars_available)
                raw = segment[self.offset : self.offset + n_chars * width]
                self.offset += n_chars * width
                remaining -= n_chars
                parts.append(raw.decode("utf-16le" if width == 2 else "latin1", "replace"))
                if remaining == 0:
                    break

            if self.offset >= len(segment):
                self.segment_index += 1
                self.offset = 0
            self._ensure()
            continuation_flag = self.segments[self.segment_index][self.offset]
            self.offset += 1
            width = 2 if (continuation_flag & 1) else 1
        return "".join(parts)


def _decode_rk(rk):
    if rk & 2:
        value = struct.unpack("<i", struct.pack("<I", rk >> 2))[0]
    else:
        value = struct.unpack("<d", struct.pack("<II", 0, rk & 0xFFFFFFFC))[0]
    return value / 100 if rk & 1 else value


def parse_biff(path):
    """Return {sheet_name: rows} for the subset of BIFF8 records used here."""
    cfb = CFB(path)
    workbook = cfb.read_stream("Workbook") or cfb.read_stream("Book")
    if workbook is None:
        raise ValueError("Workbook stream not found")

    records = []
    pos = 0
    while pos + 4 <= len(workbook):
        record_id, length = struct.unpack_from("<HH", workbook, pos)
        records.append((pos, record_id, workbook[pos + 4 : pos + 4 + length]))
        pos += 4 + length

    sheets = []
    for _, record_id, payload in records:
        if record_id == 0x0085 and len(payload) >= 8:  # BOUNDSHEET
            offset = u32(payload, 0)
            name_len = payload[6]
            flags = payload[7]
            raw = payload[8 : 8 + name_len * (2 if flags & 1 else 1)]
            name = raw.decode("utf-16le" if flags & 1 else "latin1", "ignore")
            sheets.append((name, offset))

    shared_strings = []
    for index, (_, record_id, payload) in enumerate(records):
        if record_id != 0x00FC:  # SST
            continue
        segments = [payload[8:]]
        j = index + 1
        while j < len(records) and records[j][1] == 0x003C:  # CONTINUE
            segments.append(records[j][2])
            j += 1
        unique_count = u32(payload, 4)
        cursor = SegmentCursor(segments)
        for _ in range(unique_count):
            try:
                char_count = cursor.read_u16()
                flags = cursor.read_u8()
                has_rich = bool(flags & 0x08)
                has_ext = bool(flags & 0x04)
                high_byte = bool(flags & 0x01)
                run_count = cursor.read_u16() if has_rich else 0
                ext_len = cursor.read_u32() if has_ext else 0
                text = cursor.read_chars(char_count, high_byte)
                if run_count:
                    cursor.read(run_count * 4)
                if ext_len:
                    cursor.read(ext_len)
                shared_strings.append(text)
            except Exception:
                shared_strings.append("")
                shared_strings.extend([""] * (unique_count - len(shared_strings)))
                break
        break

    result = {}
    for sheet_index, (sheet_name, start) in enumerate(sheets):
        end = sheets[sheet_index + 1][1] if sheet_index + 1 < len(sheets) else len(workbook)
        cells = {}
        pos = start
        while pos + 4 <= end:
            record_id, length = struct.unpack_from("<HH", workbook, pos)
            payload = workbook[pos + 4 : pos + 4 + length]
            pos += 4 + length
            if record_id == 0x000A:  # EOF
                break
            if record_id == 0x00FD and length >= 10:  # LABELSST
                row, col, _xf = struct.unpack_from("<HHH", payload, 0)
                sst_index = u32(payload, 6)
                cells[(row, col)] = shared_strings[sst_index] if sst_index < len(shared_strings) else ""
            elif record_id == 0x0203 and length >= 14:  # NUMBER
                row, col, _xf = struct.unpack_from("<HHH", payload, 0)
                cells[(row, col)] = struct.unpack_from("<d", payload, 6)[0]
            elif record_id == 0x027E and length >= 10:  # RK
                row, col, _xf = struct.unpack_from("<HHH", payload, 0)
                cells[(row, col)] = _decode_rk(u32(payload, 6))
            elif record_id == 0x00BD and length >= 6:  # MULRK
                row, first_col = struct.unpack_from("<HH", payload, 0)
                last_col = u16(payload, length - 2)
                offset = 4
                for col in range(first_col, last_col + 1):
                    _xf = u16(payload, offset)
                    rk = u32(payload, offset + 2)
                    offset += 6
                    cells[(row, col)] = _decode_rk(rk)
            elif record_id == 0x0204 and length >= 8:  # LABEL
                row, col, _xf, n_chars = struct.unpack_from("<HHHH", payload, 0)
                cells[(row, col)] = payload[8 : 8 + n_chars].decode("latin1", "replace")

        max_row = max((row for row, _ in cells), default=-1)
        max_col = max((col for _, col in cells), default=-1)
        result[sheet_name] = [
            [cells.get((row, col)) for col in range(max_col + 1)]
            for row in range(max_row + 1)
        ]
    return result
