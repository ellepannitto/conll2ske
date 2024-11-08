import argparse
import argcomplete
import os

from tqdm.auto import tqdm

import conll2ske.process as process

def _prova(args):
	process.foo(args.name)

def _convert(args):
	# Create output dir if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Use tqdm for progress tracking if there are multiple files
    for input_file in tqdm(args.input_files, desc="Converting files"):
        output_file = os.path.join(args.output_dir, os.path.basename(input_file) + ".vert")
        process.transform_conllu_to_vert(input_file, output_file)
        print(f"Converted {input_file} to {output_file}")

def main():
	parser = argparse.ArgumentParser(
            description= "Convert CoNLL-U files to SketchEngine compatible formats",
            add_help=True)
	
	argcomplete.autocomplete(parser)

	subparsers = parser.add_subparsers(title="actions", dest="actions")

	parser_prova = subparsers.add_parser('prova',
									  description='funzione di prova',
									  help='funzione di prova')
	parser_prova.add_argument("-n", "--name", type=str, required=True,
						   help="your name")
	parser_prova.set_defaults(func=_prova)
    
	
	parser_convert = subparsers.add_parser('convert',
                                           description='Convert CoNLL-U file to VERT format',
                                           help='Convert CoNLL-U file to VERT format')
	parser_convert.add_argument("-o", "--output-dir",
							    type=os.path.abspath,
								default=".",
								help="Output directory. Default: Current directory.")
	parser_convert.add_argument("-i", "--input-files",
							    type=os.path.abspath,
								nargs="+",
								help="Input text files.")
	parser_convert.set_defaults(func=_convert)

	args = parser.parse_args()
	if "func" not in args:
		parser.print_usage()
		exit()

	args.func(args)

if __name__ == "__main__":
    main()