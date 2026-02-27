# Uncomment line below if you need to install these packages
# install.packages(c("dplyr", "lubridate", "stringr", "tibble", "pharmaversesdtm", "admiral"))

library(dplyr, warn.conflicts = FALSE)
library(lubridate)
library(stringr)
library(tibble)
library(pharmaversesdtm)
library(admiral)
library(readr)

# Read in SDTM datasets from inputs to R
exPath <- readr::read_file("/workflow/inputs/ex")
vsPath <- readr::read_file("/workflow/inputs/vs")
admiral_adslPath <- readr::read_file("/workflow/inputs/admiral_adsl")
load(exPath)
load(vsPath)
load(admiral_adslPath)

# Prepare variables and output to .rda format
ex_ext <- ex %>%
  derive_vars_dtm(
    dtc = EXSTDTC,
    new_vars_prefix = "EXST"
  )
saveRDS(ex_ext, file="/workflow/outputs/ex_ext.rda")

vs <- vs %>%
  filter(
    USUBJID %in% c(
      "01-701-1015", "01-701-1023", "01-703-1086",
      "01-703-1096", "01-707-1037", "01-716-1024"
    ) &
      VSTESTCD %in% c("SYSBP", "DIABP") &
      VSPOS == "SUPINE"
  )
saveRDS(vs, file="/workflow/outputs/vs.rda")

adsl <- admiral_adsl %>%
  select(-TRTSDTM, -TRTSTMF)
saveRDS(adsl, file="/workflow/outputs/adsl.rda")
