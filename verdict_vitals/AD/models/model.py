from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def load_model():
    tokenizer = AutoTokenizer.from_pretrained("akhilm97/pegasus_indian_legal", use_fast=False)
    model = AutoModelForSeq2SeqLM.from_pretrained("akhilm97/pegasus_indian_legal")
    return tokenizer, model

def generate_summary(text, tokenizer, model):
    input_tokenized = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)

    summary_ids = model.generate(
        input_tokenized["input_ids"],
        num_beams=9,
        no_repeat_ngram_size=3,
        length_penalty=2.0,
        min_length=350,
        max_length=1000,
        early_stopping=True
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)
    return summary