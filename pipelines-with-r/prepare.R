library(azuremlsdk)
library(optparse)
library(caret)

print("In prepare.R")

# Get reference to this AML run to enable logging to the experiment (not needed here)
run <- get_current_run()

options <- list(
  make_option(c("--data_path_input")),
  make_option(c("--data_path_output"))
)

opt_parser <- OptionParser(option_list = options)
opt <- parse_args(opt_parser)

data <- read.csv(file = file.path(opt$data_path_input, "diabetes.csv"))

# Do data preprocessing here

if (!dir.exists(opt$data_path_output)){
  dir.create(opt$data_path_output)
}

write.csv(data, file = file.path(opt$data_path_output, "diabetes.csv"))
