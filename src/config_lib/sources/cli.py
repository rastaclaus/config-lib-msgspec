import argparse

import msgspec

from config_lib.utils.nest import nest_dict
from config_lib.utils.types import ConfigMapping


def _add_arguments(parser: argparse.ArgumentParser, struct_cls: type[msgspec.Struct], prefix: str = "") -> None:
    """Add command-line arguments to an argparse parser based on a msgspec.Struct.

    This function recursively adds arguments for each field in the given msgspec.Struct,
    handling nested structures by using dot-separated prefixes for argument names.

    Args:
        parser: The argparse.ArgumentParser to add the arguments to.
        struct_cls: The msgspec.Struct class to extract the fields from.
        prefix: The prefix to use for nested argument names (default: "").

    """
    # Iterate through the fields of the struct
    field_name: str
    field_type: type
    for field_name, field_type in struct_cls.__annotations__.items():
        # Create the full argument name (with nested prefixes)
        full_name = f"{prefix}{field_name}" if prefix else field_name

        # Handle nested msgspec.Struct types
        if issubclass(field_type, msgspec.Struct):
            # Recursively add nested arguments with dot-separated names
            _add_arguments(parser, field_type, prefix=f"{full_name}.")
        else:
            # Add a command-line argument for the field
            # Use type hints to determine argument type, defaulting to string
            parser_type: type = getattr(field_type, "__origin__", field_type)  # pyright: ignore[reportUnknownArgumentType]
            _ = parser.add_argument(
                f"--{full_name}",
                type=parser_type,
                help=f"Configuration value for {full_name}",
            )


def get_cli_values(cls: type[msgspec.Struct]) -> ConfigMapping:
    """Parse command-line arguments for a given msgspec.Struct configuration class.

    This function creates an argparse parser based on the fields of the provided
    msgspec.Struct class, allowing nested configuration through dot-separated
    argument names.

    Args:
        cls: A msgspec.Struct subclass defining the configuration structure.

    Returns:
        A ConfigMapping containing the parsed configuration values.

    Raises:
        SystemExit: If there are errors during argument parsing or validation.

    Notes:
        - Nested structures are supported through dot-separated argument names
        - Only specified arguments are processed
        - Arguments not explicitly defined are ignored

    """
    # Create an argument parser
    parser = argparse.ArgumentParser(description=f"Configuration parser for {cls.__name__}")

    # Recursively add arguments for the class and its nested structures

    # Add arguments for the top-level class
    _add_arguments(parser, cls)

    # Parse arguments
    try:
        args, _ = parser.parse_known_args()
    except SystemExit as err:
        err_details = (
            f"param '{err.__context__.args[0].dest}': {err.__context__.args[1]}"
            if err.__context__ else "unknown error"
        )
        raise ValueError(err_details) from err

    # Convert parsed arguments to a flat dictionary
    flat_args = {k: v for k, v in vars(args).items() if v is not None}

    # Convert flat dictionary to nested dictionary
    return nest_dict(flat_args, delimiter=".")
