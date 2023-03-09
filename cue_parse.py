from pyleri import (
    Grammar,
    Regex,
    Sequence,
    Choice,
    Keyword,
    Repeat,
    # Optional,
    # THIS,
)


# Define the grammar for a cue sheet file.
class CueSheetGrammar(Grammar):
    # Define regex patterns for commonly used values.
    digit_pattern = Regex('\d+')
    time_pattern = Regex('\d{2}:\d{2}:\d{2}')
    r_string_pattern = Regex('".*"')
    # rem = Sequence(Keyword('REM'), Regex('.*'))

    file_header = Sequence(
        Keyword('FILE'),
        r_string_pattern,  # Any string can follow FILE.
        Keyword('WAVE')
    )

    track_header = Sequence(
        Keyword('TRACK'),
        digit_pattern,
        Keyword('AUDIO'),
    )

    index = Sequence(
        Keyword('INDEX'),
        digit_pattern,
        time_pattern
    )

    track_meta = Choice(
        Sequence(
            Keyword('TITLE'),
            r_string_pattern  # Any string can follow TITLE.
        ),
        Sequence(
            Keyword('PERFORMER'),
            r_string_pattern  # Any string can follow PERFORMER.
        )
    )

    track = Sequence(
        track_header,
        Repeat(track_meta),
        Repeat(index),
    )
    
    # Define rules for each part of the cue sheet file.
    START = Sequence(
        Repeat(track_meta),
        file_header,
        Repeat(track),
    )

def node_props(node, children):
    return {
        # 'start': node.start,
        # 'end': node.end,
        'name': node.element.name if hasattr(node.element, 'name') else None,
        'element': node.element.__class__.__name__,
        'string': node.string,
        'children': children
    }

def get_children(children):
    return [node_props(c, get_children(c.children)) for c in children]

def view_parse_tree(res):
    start = res.tree.children[0] if res.tree.children else res.tree
    return node_props(start, get_children(start.children))

if __name__ == "__main__":
    cue_parser = CueSheetGrammar()
    # with open("profound.cue") as in_file:
    #     text = in_file.read()

    with open("profound.cue", "r", encoding='utf-8') as f:
        # read lines and filter out those that start with "REM"
        lines = [line.strip() for line in f if not line.strip().startswith("REM")]
    
        # join remaining lines into a single string
        text = "\n".join(lines)
    result = cue_parser.parse(text)
    print(result.is_valid)
    print(view_parse_tree(result))