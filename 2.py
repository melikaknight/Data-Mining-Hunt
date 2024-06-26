import csv
from sklearn import tree
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# prepare dataset
def read_dataset(filename):
    with open(filename) as csv_file:
        data = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        header = next(csv_reader)
        for row in csv_reader:
            data.append(row)
    # put labels in the last column
    header = header[1::] + [header[0]]
    data = map(lambda x:x[1::]+list(x[0]), data)

    X_data = map(lambda x:x[0:21], data)
    y_data = map(lambda x: x[22], data)
    y_data = map(int, y_data)

    return X_data, y_data


if __name__ == "__main__":
    # read dataset
    X_train, y_train = read_dataset('./Q7_Data/noisy_train.csv')
    X_train_integers = []

    X_val, y_val = read_dataset('./Q7_Data/noisy_valid.csv')
    X_val_integers = []

    X_test, y_test = read_dataset('./Q7_Data/noisy_test.csv')
    X_test_integers = []

    # convert features to integer values
    le = LabelEncoder()
    le.fit([item for sublist in X_train for item in sublist])
    for i in range(len(X_train)):
        X_train_integers.append(list(le.transform(X_train[i])))
    for i in range(len(X_val)):
        X_val_integers.append(list(le.transform(X_val[i])))
    for i in range(len(X_test)):
        X_test_integers.append(list(le.transform(X_test[i])))

    # finding proper depth (equal to post pruning)
    val_acc = []
    train_acc = []
    test_acc = []
    depth = range(1, 100)
    for d in depth:
        clf = tree.DecisionTreeClassifier(max_depth=d)
        clf.fit(X_train_integers, y_train)
        val_acc.extend([accuracy_score(y_val, clf.predict(X_val_integers))])
        train_acc.extend([accuracy_score(y_train, clf.predict(X_train_integers))])
        test_acc.extend([accuracy_score(y_test, clf.predict(X_test_integers))])

    val, = plt.plot(val_acc, 'r', label='Validation')
    train, = plt.plot(train_acc, 'g', label='Training')
    test, = plt.plot(test_acc, 'b', label='Testing')

    plt.legend(handles=[train, val, test])
    plt.title('Accuracy Vs Depth')
    plt.xlabel('Depth (proportional to number of nodes)')
    plt.ylabel('Accuracy')
    plt.show()

    optimal_depth = 5
    clf = tree.DecisionTreeClassifier(max_depth=optimal_depth)
    clf.fit(X_train_integers, y_train)
    print('--------------------------------')
    print('Validation Accuracy: ')
    print(accuracy_score(y_val, clf.predict(X_val_integers)))
    print('--------------------------------')
    print('Test Accuracy: ')
    print(accuracy_score(y_test, clf.predict(X_test_integers)))
    print('--------------------------------')
    print('Training Accuracy: ')
    print(accuracy_score(y_train, clf.predict(X_train_integers)))




