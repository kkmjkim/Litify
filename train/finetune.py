import csv
import json
import warnings

from datasets import load_dataset
from predibase import Predibase, FinetuningConfig
from tokenizers import Tokenizer

from utils import load_config

CONFIG = load_config()

warnings.filterwarnings("ignore")

pb = Predibase(api_token=CONFIG['api']['predibase'])


def convert_statue(statue: str):
    statue = statue.replace("'", '"')
    statue = json.loads(statue)
    return '\n'.join(statue)



def hfdataset_to_csv(datalist: list, csv_file_name):
    template = {
        "prompt":
            """<|im_start|>system:\n사건에 해당하는 형사법조를 찾아줘.<|im_end|>
    <|im_start|>[사건]\n {story}
    <|im_start|>[형사 법조]\n""",
        "completion": "{statutes}<|im_end|>",
        "split": "train"
    }

    with open(csv_file_name, 'w', newline='') as csvfile:
        fieldnames = template.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i, d in enumerate(datalist):
            row = {
                "prompt": template["prompt"].format(story=d['story']),
                "completion": template["completion"].format(statutes=convert_statue(d["statutes"])),
                "split": "train"
            }
            writer.writerow(row)


def validate_data_csv(csv_file_name):
    """ Make sure it has prompt, completion, and split with all values """
    with open(csv_file_name, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            assert row['prompt']
            assert row['completion']
            assert row['split']

    return True


tokenizer = Tokenizer.from_pretrained("upstage/solar-1-mini-tokenizer")


def compute_cost(csv_file_name, price_per_million_tokens=0.5):
    """ Compute the cost of the dataset """

    total_num_of_tokens = 0
    with open(csv_file_name, 'r') as f:
        reader = csv.DictReader(f)
        # get all values
        values = [row['completion'] + " " + row['prompt'] for row in reader]
        for value in values:
            # tokenize
            enc = tokenizer.encode(value)
            num_of_tokens = len(enc.tokens)
            total_num_of_tokens += num_of_tokens

    return total_num_of_tokens / 1000000 * price_per_million_tokens


hfdataset = load_dataset('csv', data_files="resource/train/train_data.csv")
train_hfdataset = hfdataset["train"]


print("Dataset not found, creating...")
dataset_name = 'litify'
csv_file_name = "resource/train/train.csv"
hfdataset_to_csv(train_hfdataset, csv_file_name)
try:
    pb_dataset = pb.datasets.get(dataset_name)
    print(f"Dataset found: {pb_dataset}")
except RuntimeError:
    print("Dataset not found, creating...")
    print(f"Dataset Validation: {validate_data_csv(csv_file_name)}")
    print(f"One step FT Cost: {compute_cost(csv_file_name)} USD")

    print("Uploading daatset...")
    pb_dataset = pb.datasets.from_file(csv_file_name, name=dataset_name)

repo_name = "litify-model"
repo = pb.repos.create(name=repo_name, description="litify", exists_ok=True)
print(repo)

# Start a fine-tuning job, blocks until training is finished
adapter = pb.adapters.create(
    config=FinetuningConfig(
        base_model="solar-1-mini-chat-240612",
    ),
    dataset=pb_dataset,  # Also accepts the dataset name as a string
    repo=repo,
    description="initial model with defaults"
)

print(adapter.repo + "/" + str(adapter.tag))
