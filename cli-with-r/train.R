library(azuremlsdk)
library(optparse)
library(caret)

print("In train.R")

# Get reference to this AML run to enable logging to the experiment
run <- get_current_run()

options <- list(
  make_option(c("--data_path"))
)

opt_parser <- OptionParser(option_list = options)
opt <- parse_args(opt_parser)

# Read data files and drop PatientID column
data_files <- list(file.path(opt$data_path, "diabetes.csv"))

data <- subset(
  do.call(rbind, lapply(data_files, read.csv)),
  select = -c(PatientID)
)

data$Diabetic <- factor(data$Diabetic)

# Train test split
set.seed(123)
idx <- createDataPartition(data$Diabetic, p = 0.75, list = FALSE)
train <- data[idx, ]
test <- data[-idx, ]

# Train model
mod <- train(
  form = Diabetic ~ .,
  data = train,
  trControl = trainControl(method = "cv", number = 5),
  method = "glm",
  family = "binomial"
)
mod

# Calculate accuracy
calc_acc <- function(actual, predicted) {
  mean(actual == predicted)
}

accuracy <- calc_acc(actual = test$Diabetic,
                     predicted = predict(mod, newdata = test))

# Log accuracy metric to run
print(accuracy)
log_metric_to_run("Accuracy", accuracy, run=run)

output_dir <- "outputs"
if (!dir.exists(output_dir)){
  dir.create(output_dir)
}

saveRDS(mod, file = "./outputs/model.rds")
message("Model saved")