import pandas as pd
from nltk.translate.bleu_score import corpus_bleu, SmoothingFunction
from nltk.translate.meteor_score import meteor_score
from rouge import Rouge

# Load your CSV file
csv_file = "trained_blip_results.csv"  # Replace with your file path
data = pd.read_csv(csv_file)

# Ensure the required columns exist
if not {'Original Description', 'Predicted Caption'}.issubset(data.columns):
    raise ValueError("CSV must contain 'Original Description' and 'Predicted Caption' columns.")

# Extract the original and predicted captions
original_captions = data['Original Description'].tolist()
predicted_captions = data['Predicted Caption'].tolist()

# Preprocessing: Tokenize captions for BLEU
original_captions_tokenized = [[caption.split()] for caption in original_captions]
predicted_captions_tokenized = [caption.split() for caption in predicted_captions]

#print(original_captions_tokenized)

# Initialize the smoothing function
smoothing_function = SmoothingFunction().method1

# BLEU Score
corpus_bleu_score = corpus_bleu(
    original_captions_tokenized, 
    predicted_captions_tokenized,
    smoothing_function=smoothing_function
)
print(f"Corpus BLEU Score: {corpus_bleu_score:.4f}")

# METEOR Score
meteor_scores = [
    meteor_score([orig.split()], pred.split())
    for orig, pred in zip(original_captions, predicted_captions)
]
avg_meteor_score = sum(meteor_scores) / len(meteor_scores)
print(f"Average METEOR Score: {avg_meteor_score:.4f}")

# ROUGE Scores
rouge = Rouge()
rouge_scores = rouge.get_scores(predicted_captions, original_captions, avg=True)
print("ROUGE Scores:")
print(f"  ROUGE-1: {rouge_scores['rouge-1']}")
print(f"  ROUGE-2: {rouge_scores['rouge-2']}")
print(f"  ROUGE-L: {rouge_scores['rouge-l']}")

# Save results to a CSV file
output_file = "evaluation_scores.csv"
evaluation_results = {
    "Metric": ["BLEU","METEOR", "ROUGE-1", "ROUGE-2", "ROUGE-L"],
    "Score": [
        corpus_bleu_score,
        avg_meteor_score,
        rouge_scores["rouge-1"]["f"],
        rouge_scores["rouge-2"]["f"],
        rouge_scores["rouge-l"]["f"],
    ]
}
results_df = pd.DataFrame(evaluation_results)
results_df.to_csv(output_file, index=False)
print(f"Evaluation results saved to {output_file}")
