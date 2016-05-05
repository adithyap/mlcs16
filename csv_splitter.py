import os
import helper


def split_csv(input_file, max_chunk_size=60000):

    target_file_dir = os.path.dirname(input_file)
    target_file_prefix = helper.get_name_without_extension(input_file)

    current_chunk_size = 0
    current_chunk_index = 1
    header_str = ''
    b_first = True

    f_in = open(input_file, 'r')
    f_out = None

    for line in f_in:

        if b_first:

            # Read header for the first time alone and don't do anything else there
            header_str = line
            b_first = False
            continue

        if current_chunk_size == 0:

            # Create new file with chunk index
            target_file_name = target_file_prefix + '_' + str(current_chunk_index) + '.csv'
            target_file_path = os.path.join(target_file_dir, target_file_name)

            if f_out is not None:
                f_out.close()

            f_out = open(target_file_path, 'w')

            # Write header
            f_out.write(header_str)

        # Write current line
        f_out.write(line)

        # Validate chunk size
        current_chunk_size += 1

        if current_chunk_size >= max_chunk_size:
            current_chunk_size = 0
            current_chunk_index += 1

    f_in.close()


def main():

    input_file = 'csv_data/BloombergVOTELEVEL_Touse.csv'

    split_csv(input_file)


if __name__ == '__main__':
    main()
