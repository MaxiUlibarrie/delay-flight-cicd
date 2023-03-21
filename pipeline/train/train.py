import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
import xgboost as xgb
import joblib

from common.config_handler import Config
from common.log_handler import Logger
from common.reports import confusion_matrix_pretty, classification_report_pretty

logger = Logger()
config = Config()

TEST_SIZE = config.get.train.test_size_split
MODEL_TYPE = config.get.train.model_type
PREFIX_FEATURE_VALUE = config.get.base.separator_feature_value
PARAMETERS_GRID_SEARCH_XGBOOST = vars(config.get.train.parameters_GridSearch.xgboost)
FEATURE_CATEGORIC_BASIC = list(config.get.base.features.categoric)
TARGET_NAME = config.get.base.features.target

MODEL_TYPE_LIST = config.get.train.model_type_list
if not MODEL_TYPE in MODEL_TYPE_LIST:
    msg = f"Model Type: {MODEL_TYPE} does not exists or is not implemented."
    logger.log.error(msg)
    raise RuntimeError(msg)

logger.log.info("Retrieving training data.")
data = pd.read_csv('./data/train.csv')

data = shuffle(data[FEATURE_CATEGORIC_BASIC + [TARGET_NAME]], random_state = 111)

dummies_list = [ pd.get_dummies(data[f], prefix=f, prefix_sep=PREFIX_FEATURE_VALUE) for f in FEATURE_CATEGORIC_BASIC ]

features_df = pd.concat(dummies_list, axis = 1)
label = data[TARGET_NAME]

x_train, x_test, y_train, y_test = train_test_split(features_df, label, 
                                                    test_size = TEST_SIZE, 
                                                    random_state = 42)

model = None
logger.log.info(f"Training {MODEL_TYPE} model.")
if MODEL_TYPE == 'LOG_REG':
    logReg = LogisticRegression()
    model = logReg.fit(x_train, y_train)
elif MODEL_TYPE == 'XGBOOST':
    parameters = PARAMETERS_GRID_SEARCH_XGBOOST

    xgb_model = xgb.XGBClassifier(random_state=1, max_depth = 10)

    modelxgb_GridCV = GridSearchCV(xgb_model, param_grid = parameters, 
                                   cv = 2, n_jobs=-1, verbose=1).fit(x_train, y_train)
    
    model = modelxgb_GridCV.best_estimator_

model.feature_names_final = list(x_train.columns.values)

y_pred = model.predict(x_test)

conf_m_report = confusion_matrix_pretty(y_test, y_pred)
clf_report = classification_report_pretty(y_test, y_pred)

logger.log.info("Confussion Matrix:")
logger.log.info("\n" + str(conf_m_report))

logger.log.info("Classification Report:")
logger.log.info("\n" + str(clf_report))

logger.log.info("Saving model.")
joblib.dump(model, 'models/model_delay_flight.pkl')
