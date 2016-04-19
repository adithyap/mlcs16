import helper
import generate_case_data
import generate_n_grams
import time
import os

files = [x for x in helper.get_files('.') if x.endswith('_complete.zip')]

save_dir = 'data'
helper.ensure_dir(save_dir)

for f in files:

    start = time.time()

    f_name = helper.unzip_file(f)

    # Create titles
    case_data_dir = generate_case_data.process_dir(f_name, b_size=2)

    print('Completed extracting case data from ' + f_name)

    # Create n_grams
    n_gram_dir = generate_n_grams.process_dir(case_data_dir, 2, 4, b_verbose=True, b_size=2)

    print('Completed generating n_grams from ' + f_name)

    helper.move_dir(n_gram_dir, os.path.join(save_dir, f_name))

    print('Completed processing ' + str(f_name) + ' in ' + str(time.time() - start) + ' (s)')

    helper.delete_dir(f_name)

    break




