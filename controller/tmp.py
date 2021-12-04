import slcan_converter as sc

print(sc.format_from_slcan("t2342ABCD"))
print(sc.format_from_slcan("T1234ABCD3ABCDEF"))
print(sc.format_from_slcan("r234811223344AABBCCDD"))
print(sc.format_from_slcan("R1234ABCD6AABBCCDD1122"))

print(sc.convert_to_slcan(0x675, [0x22, 0xAB, 0xCD, 0xDE, 0xEAD]))
