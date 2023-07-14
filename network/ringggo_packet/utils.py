def convert_bytes_to_hexstring(source: bytes):
    if source is None:
        return ""

    result_string = ""

    character_count = 0
    for byte in source:
        result_string += str(hex(byte)) + " "
        character_count += 1
        if character_count % 8 == 0:
            result_string += "\n"
    return result_string.strip()
