import csv
from collections import defaultdict, OrderedDict


def download(dataset):
    # it seems like data needs to be downloaded manually under https://smallworldofwords.org/en/project/research
    pass


def extract_data(filename, mappings):
    data = defaultdict(lambda: defaultdict(int))

    try:
        with open(filename) as f:
            reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            for row in reader:
                cue = row.get("cue")
                response = row.get("response")
                value = int(row.get("R123") or row.get("R1"))
                cue_res = mappings["en"][cue]
                response_res = mappings["en"][response]
                if cue_res and response_res:
                    cue_id = cue_res[0][0]
                    response_id = response_res[0][0]
                    data[(cue_id, cue)][response_id] = value
    except FileNotFoundError:
        print(f"Data needs to be downloaded manually under https://smallworldofwords.org/en/project/research")

    return data


def map(dataset, concepticon, mappings):
    r1_data = extract_data(dataset.raw_dir / "strength.SWOW-EN.R1.20180827.csv", mappings)
    r123_data = extract_data(dataset.raw_dir / "strength.SWOW-EN.R123.20180827.csv", mappings)

    table = []

    for concepticon_id, cue in r1_data.keys() | r123_data.keys():
        concepticon_gloss = concepticon.conceptsets[concepticon_id].gloss
        r1 = dict(r1_data[(concepticon_id, cue)])
        r123 = dict(r123_data[(concepticon_id, cue)])
        row = OrderedDict([
            ("CONCEPTICON_ID", concepticon_id),
            ("CONCEPTICON_GLOSS", concepticon_gloss),
            ("ENGLISH", cue),
            ("R1", r1),
            ("R123", r123)
        ])
        table.append(row)

    dataset.table.write(table)
