import csv
from collections import defaultdict, OrderedDict


def download(dataset):
    # it seems like data needs to be downloaded manually under https://smallworldofwords.org/en/project/research
    pass


def map(dataset, concepticon, mappings):
    r1_data = defaultdict(lambda: defaultdict(int))
    r123_data = defaultdict(lambda: defaultdict(int))

    with open(dataset.raw_dir / "associationData.csv") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            cue = row["cue"]
            response1 = row["asso1"]
            response2 = row["asso2"]
            response3 = row["asso3"]
            cue_res = mappings["nl"][cue]
            if not cue_res:
                continue
            cue_id = cue_res[0][0]
            response1_res = mappings["nl"][response1]
            if response1_res:
                response1_id = response1_res[0][0]
                r1_data[(cue_id, cue)][response1_id] += 1
                r123_data[(cue_id, cue)][response1_id] += 1
            response2_res = mappings["nl"][response2]
            if response2_res:
                response2_id = response2_res[0][0]
                r123_data[(cue_id, cue)][response2_id] += 1
            response3_res = mappings["nl"][response3]
            if response3_res:
                response3_id = response3_res[0][0]
                r123_data[(cue_id, cue)][response3_id] += 1

    table = []

    for concepticon_id, cue in r1_data.keys() | r123_data.keys():
        concepticon_gloss = concepticon.conceptsets[concepticon_id].gloss
        r1 = dict(r1_data[(concepticon_id, cue)])
        r123 = dict(r123_data[(concepticon_id, cue)])
        row = OrderedDict([
            ("CONCEPTICON_ID", concepticon_id),
            ("CONCEPTICON_GLOSS", concepticon_gloss),
            ("DUTCH", cue),
            ("R1", r1),
            ("R123", r123)
        ])
        table.append(row)

    dataset.table.write(table)
