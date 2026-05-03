def parse_args_to_dict(args):
    result = {}
    alone_index = 1
    i = 0

    while i < len(args):
        item = args[i]

        if len(item) > 1 and item[0] == "-":
            key = item[1:]

            if key == "":
                result[str(alone_index)] = item
                alone_index += 1
                i += 1
                continue

            if i + 1 < len(args):
                next_item = args[i + 1]

                if len(next_item) > 0 and next_item[0] == "-":
                    result[key] = True
                    i += 1
                else:
                    result[key] = next_item
                    i += 2
            else:
                result[key] = True
                i += 1

        else:
            result[str(alone_index)] = item
            alone_index += 1
            i += 1

    return result