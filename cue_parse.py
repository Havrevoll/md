from pprint import pprint
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

    tracks = Sequence(
        track_header,
        Repeat(track_meta),
        Repeat(index),
    )
    
    disc_header = Repeat(track_meta)

    # Define rules for each part of the cue sheet file.
    START = Sequence(
        disc_header,
        file_header,
        Repeat(tracks),
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

def find_elem(tree, name):
    for i, a in enumerate(tree['children']):
        if len(a['children']) > 0 and a['children'][0]['string'] == name:
            return a['children'][1]['string']
        elif len(a['children']) > 0:
            return find_elem(a, name)
    return None

cue_parser = CueSheetGrammar()
            
def cue_parse(file):
    with open(file, "r", encoding='utf-8') as f:
        # read lines and filter out those that start with "REM"
        lines = [line.strip() for line in f if not line.strip().startswith("REM")]
    
        # join remaining lines into a single string
        text = "\n".join(lines)
    result = cue_parser.parse(text)
    assert result.is_valid
    tre = view_parse_tree(result)
 
    res_disc_title = find_elem(tre['children'][0], "TITLE")
    res_disc_performer = find_elem(tre['children'][0], "PERFORMER")
    res_track_number = len(tre['children'][2])
    res_tracks = []
    for i in range(res_track_number):
        track_entry = tre['children'][2]['children'][i]['children']
        track_dict = {}
        track_dict['title'] = find_elem(track_entry[1], "TITLE")
        track_dict['performer'] = find_elem(track_entry[1], "PERFORMER")
        track_dict['number'] = int(track_entry[0]['children'][1]['string'])
        assert int(track_entry[2]['children'][-1]['children'][1]['string']) == 1
        track_dict['index'] = track_entry[2]['children'][-1]['children'][2]['string']
        res_tracks.append(track_dict)        
    return {'title':res_disc_title,'performer':res_disc_performer, 'tracks':res_tracks}


if __name__ == "__main__":
    disc = cue_parse("profound.cue")
    print(disc)