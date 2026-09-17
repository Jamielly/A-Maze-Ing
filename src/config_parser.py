from dataclasses import dataclass


@dataclass
class ConfigData:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    animate: bool = False
    seed: int | None = None


class ConfigParser:
    def __init__(self, filepath: str) -> None:
        self.filepath: str = filepath

    def parse(self) -> ConfigData:
        raw_config: dict[str, str] = {}

        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        raise ValueError(
                            f"Invalid line format (missing '='): '{line}'"
                        )
                    key, value = line.split("=", 1)
                    raw_config[key.strip().upper()] = value.strip()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Configuration file '{self.filepath}' not found."
            )
        except OSError as e:
            raise OSError(
                f"Error reading configuration file '{self.filepath}': {e}"
            )

        mandatory_keys = [
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
        ]
        for key in mandatory_keys:
            if key not in raw_config:
                raise ValueError(f"Missing mandatory configuration key: {key}")

        try:
            width = int(raw_config["WIDTH"])
            height = int(raw_config["HEIGHT"])
        except ValueError:
            raise ValueError("WIDTH and HEIGHT must be valid integers.")

        if width <= 0 or height <= 0:
            raise ValueError("WIDTH and HEIGHT must be positive integers.")

        try:
            entry_parts = raw_config["ENTRY"].split(",")
            if len(entry_parts) != 2:
                raise ValueError
            entry = (int(entry_parts[0].strip()), int(entry_parts[1].strip()))
        except (ValueError, AttributeError):
            raise ValueError(
                "ENTRY must be in 'x,y' integer coordinate format."
            )

        try:
            exit_parts = raw_config["EXIT"].split(",")
            if len(exit_parts) != 2:
                raise ValueError
            exit_pos = (
                int(exit_parts[0].strip()),
                int(exit_parts[1].strip()),
            )
        except (ValueError, AttributeError):
            raise ValueError(
                "EXIT must be in 'x,y' integer coordinate format."
            )

        if not (0 <= entry[0] < width and 0 <= entry[1] < height):
            raise ValueError(
                f"ENTRY coordinates {entry} are out of bounds "
                f"for grid size {width}x{height}."
            )

        if not (0 <= exit_pos[0] < width and 0 <= exit_pos[1] < height):
            raise ValueError(
                f"EXIT coordinates {exit_pos} are out of bounds "
                f"for grid size {width}x{height}."
            )

        if entry == exit_pos:
            raise ValueError("ENTRY and EXIT coordinates must be different.")

        perfect_str = raw_config["PERFECT"].lower()
        if perfect_str in ("true", "1", "yes"):
            perfect = True
        elif perfect_str in ("false", "0", "no"):
            perfect = False
        else:
            raise ValueError(
                "PERFECT must be a boolean value (True or False).")

        output_file = raw_config["OUTPUT_FILE"]
        if not output_file:
            raise ValueError("OUTPUT_FILE path cannot be empty.")

        animate = False
        if "ANIMATE" in raw_config:
            animate_str = raw_config["ANIMATE"].lower()
            if animate_str in ("true", "1", "yes"):
                animate = True
            elif animate_str in ("false", "0", "no"):
                animate = False
            else:
                raise ValueError(
                    "ANIMATE must be a boolean value (True or False)."
                )

        seed: int | None = None
        if "SEED" in raw_config:
            try:
                seed = int(raw_config["SEED"])
            except ValueError:
                raise ValueError("SEED must be a valid integer.")

        return ConfigData(
            width=width,
            height=height,
            entry=entry,
            exit=exit_pos,
            output_file=output_file,
            perfect=perfect,
            animate=animate,
            seed=seed,
        )
