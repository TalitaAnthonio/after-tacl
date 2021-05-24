# 3 epochs trainen = 15 minuten ongeveer op de gpu 

from torch.utils.data import DataLoader, TensorDataset
from transformers import DistilBertForSequenceClassification, AdamW, DistilBertTokenizerFast, BertTokenizer, BertForSequenceClassification
import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from pathlib import Path
import pdb
import pandas as pd 
from torch.nn.utils.rnn import pad_sequence

NUM_EPOCHS = 10
DEVICE = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
TEST_DF = pd.read_csv("./test.csv")
TRAIN_DF = pd.read_csv("./train.csv")
DEV_DF = pd.read_csv("./validation.csv")
TOKENIZER = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
optimizer = AdamW(model.parameters(), lr=2e-5, correct_bias=False)

def convert_labels(list_with_labels, binary=False): 
    list_of_converted_labels = []
    
    entails = ['equivalence', 'forward_entailment', 'reverse_entailment']

    if binary: 
        for label in list_with_labels: 
            if label == 'equivalence': 
                list_of_converted_labels.append(0)
            elif label == 'alternation': 
                list_of_converted_labels.append(1)
            elif label == 'other-related': 
                list_of_converted_labels.append(2)
            elif label == 'independent': 
                list_of_converted_labels.append(3)
            elif label == 'forward_entailment': 
                list_of_converted_labels.append(4)
            elif label == 'reverse_entailment': 
                list_of_converted_labels.append(5)
            else: 
                print("there is an errror")
                pdb.set_trace()
    
        return list_of_converted_labels
    
    else: 
        print("using binary .... ")
        binary_list = [1 if label in entails else 0 for label in list_with_labels]
        return binary_list



def read_entailment_data(dataframe):
    """
        Returns a list with texts [" ", " "]
        and a parallel list with labels [1,0,1, ....., ]
    """
    #'equivalence', 'alternation', 'other-related', 'independent', 'forward_entailment', 'reverse_entailment'}
    dataframe['context_x'] = dataframe['context_x'].apply(lambda x : x.replace("<x>", "").replace("</x>", ""))
    dataframe['context_y'] = dataframe['context_y'].apply(lambda x : x.replace("<y>", "").replace("</y>", ""))
    x_texts = dataframe['context_x'].tolist()
    y_texts = dataframe['context_y'].tolist()
    labels = convert_labels(dataframe['semantic_rel'].tolist())
    return x_texts, y_texts, labels 


def train(model, optim, train_loader, DEVICE, num_epochs=3): 
    epoch_loss = 0 
    epoch_acc = 0 
    for (pair_token_ids, mask_ids, seg_ids, y) in train_loader:
        optim.zero_grad()

        # [16,249]
        input_ids = pair_token_ids.to(DEVICE)
        
        # [16,9] -> deze heeft niet de juiste dimensie
        attention_mask = mask_ids.to(DEVICE)

        # 16,9
        seg_ids = seg_ids.to(DEVICE)
        # 16
        labels = y.to(DEVICE)

        outputs = model(input_ids, token_type_ids=seg_ids, attention_mask=attention_mask, labels=labels)

        loss = outputs.loss
        logits = outputs.logits 
        
        # add the loss to the item. 
        epoch_loss += loss.item()

        # compute the accuracy 
        accuracy_score = compute_accuracy(labels, logits)
        epoch_acc += accuracy_score

        loss.backward()
        optim.step()

    
    print("total loss {0} and accuracy {1}".format(epoch_loss/len(train_loader), epoch_acc/len(train_loader)  ))
    return epoch_loss/len(train_loader), epoch_acc / len(train_loader)

def evaluate(model, valid_loader, DEVICE): 

    epoch_loss = 0 
    epoch_acc = 0 

    with torch.no_grad(): 

        for (pair_token_ids, mask_ids, seg_ids, y) in valid_loader: 
            input_ids = pair_token_ids.to(DEVICE)
        
            # [16,9] -> deze heeft niet de juiste dimensie
            attention_mask = mask_ids.to(DEVICE)

            # 16,9
            seg_ids = seg_ids.to(DEVICE)
             # 16
            labels = y.to(DEVICE)

            outputs = model(input_ids, token_type_ids=seg_ids, attention_mask=attention_mask, labels=labels)
           
            loss = outputs.loss
            logits = outputs.logits 
            
            # add the loss to the item. 
            epoch_loss += loss.item()

            # compute the accuracy 
            accuracy_score = compute_accuracy(labels, logits)
            epoch_acc += accuracy_score
            
    print("total loss {0} and accuracy {1}".format(epoch_loss/len(valid_loader), epoch_acc/len(valid_loader)  ))
    return epoch_loss/len(valid_loader), epoch_acc / len(valid_loader)

def compute_accuracy(labels, logits): 
    """
        Predicted: tensor with logits [[], [], []] of shape [batch_size, label_size]
    """
    accuracy = (logits.max(1).indices  == labels).sum().item() / logits.size(0)

    return accuracy

def encode_data(x_context, y_context, labels): 

    token_ids = []
    mask_ids = []
    seg_ids = []

    for (x, y) in zip(x_context, y_context): 
        x_encoded = TOKENIZER(x, add_special_tokens=False)
        y_encoded = TOKENIZER(y, add_special_tokens=False)

        #  [CLS] sentence1 [SEP] sentence2 [SEP]

        pair_token_ids = [TOKENIZER.cls_token_id] + x_encoded['input_ids'] + [TOKENIZER.sep_token_id] + y_encoded['input_ids'] + [TOKENIZER.sep_token_id]
        

        x_length = len(x_encoded['input_ids'])
        y_length = len(y_encoded['input_ids'])
        segment_ids = torch.tensor([0] * (x_length + 2) + [1] * (y_length + 1))  # sentence 0 and sentence 1
        attention_mask_ids = torch.tensor([1] * (x_length + y_length + 3))  # mask padded values


        token_ids.append(torch.tensor(pair_token_ids))
        seg_ids.append(segment_ids)
        mask_ids.append(attention_mask_ids)

    token_ids = pad_sequence(token_ids, batch_first=True)
    mask_ids = pad_sequence(mask_ids, batch_first=True)
    seg_ids = pad_sequence(seg_ids, batch_first=True)
    labels = torch.tensor(labels)
    dataset = TensorDataset(token_ids, mask_ids, seg_ids, labels)

    return dataset




def main(): 
    x_context_train, y_context_train, labels_train = read_entailment_data(TRAIN_DF)
    x_context_test, y_context_test, labels_test = read_entailment_data(TEST_DF)
    x_context_dev, y_context_dev, labels_dev = read_entailment_data(DEV_DF)

    train_encoded = encode_data(x_context_train, y_context_train, labels_train)
    test_encoded = encode_data(x_context_test, y_context_test, labels_test)
    dev_encoded =  encode_data(x_context_dev, y_context_dev, labels_dev)

    test_loader = DataLoader(test_encoded, shuffle=True, batch_size=16)
    train_loader = DataLoader(train_encoded, shuffle=True, batch_size=16)
    dev_loader = DataLoader(dev_encoded, shuffle=True, batch_size=16)


    print("------------training --------------------------------------")
    
    #model.to(DEVICE)
    #model.train()
    #optim = AdamW(model.parameters(), lr=5e-5)
    #for epoch, _ in enumerate(range(NUM_EPOCHS),1):
    #    print("------- epoch {0}".format(epoch))
    #    
    #    train(model, optim, train_loader, DEVICE)
    #print("training is finished")

    model = torch.load("bertforentailment.pt")

    print("=============evaluating ========================================")
    model.eval()
    for epoch, _ in enumerate(range(NUM_EPOCHS),1):
         print("------- epoch {0}".format(epoch))
         evaluate(model, dev_loader, DEVICE)

main()
