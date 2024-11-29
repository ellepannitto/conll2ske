import os
import argparse
import argcomplete
import json
import regex as re

from tqdm.auto import tqdm
import tools.validate as tools

import conll2ske.process as process

def _prova(args):
	process.foo(args.name)

def _convert(args) -> None:
	# Create output dir if it doesn't exist
	os.makedirs(args.output_dir, exist_ok=True)

	tagsets = {tools.XPOS:None,
			tools.UPOS:None,
			tools.FEATS:None,
			tools.DEPREL:None,
			tools.DEPS:None,
			tools.TOKENSWSPACE:None,
			tools.AUX:None}

	if args.lang:
		tagsets[tools.UPOS] = tools.load_upos_set('cpos.ud')
		tagsets[tools.FEATS] = tools.load_feat_set('feats.json', args.lang)
		tagsets[tools.DEPREL] = tools.load_deprel_set('deprels.json', args.lang)
		tagsets[tools.DEPS] = tools.load_edeprel_set('edeprels.json', args.lang, tagsets[tools.DEPREL])
		tagsets[tools.TOKENSWSPACE] = tools.load_set('tokens_w_space.ud', 'tokens_w_space.'+args.lang)
		tagsets[tools.TOKENSWSPACE] = [re.compile(regex) for regex in tagsets[tools.TOKENSWSPACE]] #...turn into compiled regular expressions
		with open(os.path.join(tools.THISDIR, 'data', 'data.json'), 'r', encoding='utf-8') as f:
			jsondata = json.load(f)
		auxdata = jsondata['auxiliaries']
		tagsets[tools.AUX], tagsets[tools.COP] = tools.get_auxdata_for_language(args.lang)

	for input_file in tqdm(args.input_files, desc="Validating files"):
		tools.validate(open(input_file), None, args, tagsets, set())

	# Use tqdm for progress tracking if there are multiple files
	for input_file in tqdm(args.input_files, desc="Converting files"):
		output_file = os.path.join(args.output_dir,
								   os.path.basename(input_file).replace('.conllu', '.vert'))
		process.transform_conllu_to_vert(input_file, output_file)
		print(f"Converted {input_file} to {output_file}")

def main() -> None:
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


	parser_convert: argparse.ArgumentParser = subparsers.add_parser('convert',
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
	parser_convert.add_argument("--lang",
							 action="store", required=True, default=None,
							 help="""Which langauge are we checking?
							 If you specify this (as a two-letter code), the tags will be checked
							 using the language-specific files in the
							 data/directory of the validator.""")
	parser_convert.add_argument("--level", action="store", type=int, default=5, dest="level",
							 help="Level 1: Test only CoNLL-U backbone. Level 2: UD format. Level 3: UD contents. Level 4: Language-specific labels. Level 5: Language-specific contents.")
	parser_convert.add_argument("--no-tree-text", action="store_false", default=True, dest="check_tree_text",
							 help="Do not test tree text. For internal use only, this test is required and on by default.")
	parser_convert.add_argument('--coref', action='store_true', default=False, dest='check_coref',
							  help='Test coreference and entity-related annotation in MISC.')
	parser_convert.add_argument("--no-space-after", action="store_false", default=True, dest="check_space_after",
							 help="Do not test presence of SpaceAfter=No.")
	parser_convert.set_defaults(func=_convert)

	args = parser.parse_args()
	if "func" not in args:
		parser.print_usage()
		exit()

	args.func(args)

if __name__ == "__main__":
	main()
