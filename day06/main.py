if __name__ == '__main__':
    with open('input.txt') as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    for line in input_data:
        packet_found = False
        message_found = False
        for char_index,char in enumerate(line):
            if not packet_found:
                current_four = line[char_index:char_index+4]
                if len(set(current_four)) == 4:
                    packet_found = True
                    print(f"Start of packet found at index {char_index+4} as sequence '{current_four}'")
            if not message_found:
                current_fourteen = line[char_index:char_index+14]
                if len(set(current_fourteen)) == 14:
                    message_found = True
                    print(f"Start of message found at index {char_index+14} as sequence '{current_fourteen}'")
        if packet_found and message_found: break
