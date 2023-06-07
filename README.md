# refcooker

This package is meant for retriving the literature on some topic, based on a personal bibliography.

## Usage

You don't need to install anything. For example, to list the available papers on GWTC-3, simply write:

    python oven.py --query gwtc-3

To see the available tags:

    python oven.py --options 1
    
To add a new reference to the bibliography:

    python oven.py --add-reference 1 --arxiv <1970.1234> --author <chandrasekhar+> --year <1970> --tag <black-holes> <perturbations> ...

That's all!
