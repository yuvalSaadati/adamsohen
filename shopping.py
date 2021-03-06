import csv
from datetime import datetime

from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
TEST_SIZE = 0.4
import pandas as pd
def main():
    data = pd.read_csv('shopping.csv')
    # Load data and split into train and test sets
    evidence, labels = load_data("shopping.csv")
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model
    model = train_model(X_train, y_train)
    # Make predictions
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")
    count_weekend_revenue=0
    count_weekend=0
    count_revenue=0

    for rowIndex, row in data.iterrows():  # iterate over rows
        if row['Weekend'] and row['Revenue']:
            count_weekend_revenue+=1
        if row['Weekend'] :
            count_weekend += 1
        if row['Revenue'] :
            count_revenue += 1
    print("amount of people on the weekend and revenue : " + str(count_weekend_revenue))
    print("amount of people on the weekend : " + str(count_weekend))
    print("amount of people revenue : " + str(count_revenue))
    print("total data: "+str(data.__len__()))

def load_data(filename):
    """
    Load shopping data from a CSV file `shopping.csv` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).
    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)
    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open("shopping.csv", "r") as infile:
        reader = csv.DictReader(infile)
        evidence = []
        labels = []
        for line in reader:
            currEvidence = []
            currEvidence.append(int(line["Administrative"]))
            currEvidence.append(float(line["Administrative_Duration"]))
            currEvidence.append(int(line["Informational"]))
            currEvidence.append(float(line["Informational_Duration"]))
            currEvidence.append(int(line["ProductRelated"]))
            currEvidence.append(float(line["ProductRelated_Duration"]))
            currEvidence.append(float(line["BounceRates"]))
            currEvidence.append(float(line["ExitRates"]))
            currEvidence.append(float(line["PageValues"]))
            currEvidence.append(float(line["SpecialDay"]))
            currEvidence.append(datetime.strptime(line["Month"][:3], "%b").month - 1)
            currEvidence.append(int(line["OperatingSystems"]))
            currEvidence.append(int(line["Browser"]))
            currEvidence.append(int(line["Region"]))
            currEvidence.append(int(line["TrafficType"]))
            currEvidence.append(1 if line["VisitorType"] == "Returning_Visitor" else 0)
            currEvidence.append(1 if line["Weekend"] == "TRUE" else 0)

            evidence.append(currEvidence)
            labels.append(1 if line["Revenue"] == "TRUE" else 0)

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
   # model = KMeans(n_clusters=2) # KMeans
    model = GaussianNB() #Naive Bayes
    #Model = KNeighborsClassifier(n_neighbors=1) #KNN
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).
    Assume each label is either a 1 (positive) or 0 (negative).
    `sensitivity` should be a value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.
    `specificity` should be a value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    trueNegatives = 0
    truePositives = 0
    for label, prediction in zip(labels, predictions):
        if label == 1 and prediction == 1:
            truePositives += 1
        elif label == 0 and prediction == 0:
            trueNegatives += 1

    return (truePositives / len(labels), trueNegatives / len(labels))


if __name__ == "__main__":
    main()