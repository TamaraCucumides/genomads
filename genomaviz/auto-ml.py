from sklearn.model_selection import train_test_split



# MODELOS
# CLASIFICACION: random forest, svm, decision tree, logistic regression
# REGRESION: linear regression, random forest, svr, naive bayes?
# RANKEO: lightgbm-ltr

def genomaML_class(X, y, test_split=0.15):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_split, random_state=42)

def genomaML_regr(X , y, test_split=0.15):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_split, random_state=42)

def genomaML_ltr(X , y, test_split=0.15):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_split, random_state=42)