import itertools


alphabet = [chr(i) for i in range(255)]


def compress(alphabet):
    """
    Generator for compressing data taken by the send() method. When empty data is sent it raises
    StopIteration Exception. This generator needs to be primed firstly.
    """

    # make initial dictionary {word: position_in_alphabet} from alphabet
    dictionary = {s: pos for pos, s in enumerate(alphabet)}
    alphabet_size = len(alphabet) - 1
    compressed_table = []

    while True:
        # here data is taken from user and yielded after processing
        text = yield compressed_table
        if not text:
            return []

        compressed_table = []
        word = ''
        for sign in text:
            ws = word + sign

            if ws in dictionary:
                word = ws
            else:
                compressed_table.append(dictionary[word])
                alphabet_size += 1
                dictionary[ws] = alphabet_size
                word = sign

        if word:
            compressed_table.append(dictionary[word])


def decompress(alphabet):
    """
    Generator for decompressing encoded data taken by the send() method. Works conversely to compress function.
    """

    # make initial dictionary {position_in_alphabet: word}
    dictionary = {pos: s for pos, s in enumerate(alphabet)}
    alphabet_size = len(alphabet) - 1
    decompressed_text = ''

    while True:
        # here data is send by use and yielded after processing
        compressed_table = yield decompressed_text
        if not compressed_table:
            return ''

        prev_code = compressed_table[0]
        decompressed_text = dictionary[prev_code]

        for code in itertools.islice(compressed_table, 1, None):
            prev_word = dictionary[prev_code]

            alphabet_size += 1
            if code in dictionary:
                output = dictionary[code]
                dictionary[alphabet_size] = prev_word + dictionary[code][0]
            else:
                output = prev_word + prev_word[0]
                dictionary[alphabet_size] = output

            decompressed_text += output
            prev_code = code


def compress_file(input_file_name, output_file_name):
    """
    Function for lazy compression. It lazily fetches rows from input file and save it in the same approach
    to save the memory.
    """
    with open(input_file_name, 'r') as read_file, open(output_file_name, 'w+') as write_file:
        compressor_gen = compress(alphabet)
        # priming generator
        next(compressor_gen)
        for line in read_file:
            compressed = compressor_gen.send(line)
            write_file.write(" ".join([str(c) for c in compressed]) + '\n')
        compressor_gen.close()


def decompress_file(input_file_name, output_file_name):
    """
    Function for lazy decompression. It lazily decompress file encoded by compress_file function.
    """
    with open(input_file_name, 'r') as read_file, open(output_file_name, 'w+') as write_file:
        decompress_gen = decompress(alphabet)
        # priming generator
        next(decompress_gen)
        for line in read_file:
            decompressed = decompress_gen.send([int(s) for s in line.split()])
            write_file.write(decompressed)
        decompress_gen.close()

compress_file('input', 'compressed')
decompress_file('compressed', 'decompressed')