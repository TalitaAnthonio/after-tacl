import spacy 


def count_tags(pos_tagged_fillers): 
    list_with_sequences = []
    
    all_pos_tags = []
    all_token_sequences = []
    for elem in pos_tagged_fillers: 
        sequence_of_pos_tags = []
        sequence_of_tokens = []
        for token, pos in elem: 
            sequence_of_pos_tags.append(pos)
            sequence_of_tokens.append(token)
        all_pos_tags.append(" ".join(sequence_of_pos_tags))
        all_token_sequences.append(sequence_of_tokens)
    return all_pos_tags, all_token_sequences

