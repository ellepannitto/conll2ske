import argparse
import argcomplete

import conll2ske.process as process

def _prova(args):
	process.foo(args.name)

def main():
	parser = argparse.ArgumentParser(add_help=True)
	argcomplete.autocomplete(parser)

	subparsers = parser.add_subparsers(title="actions", dest="actions")

	parser_prova = subparsers.add_parser('prova',
									  description='funzione di prova',
									  help='funzione di prova')
	parser_prova.add_argument("-n", "--name", type=str, required=True,
						   help="your name")
	parser_prova.set_defaults(func=_prova)

	args = parser.parse_args()
	if "func" not in args:
		parser.print_usage()
		exit()

	args.func(args)