library(dplyr, warn.conflicts = FALSE)
library(lubridate)
library(stringr)
library(tibble)
library(pharmaversesdtm)
library(admiral)

ex_ext <- readRDS("/workflow/inputs/ex_ext")
adsl <- readRDS("/workflow/inputs/adsl")

adsl <- adsl %>%
  derive_vars_merged(
    dataset_add = ex_ext,
    filter_add = !is.na(EXSTDTM),
    new_vars = exprs(TRTSDTM = EXSTDTM, TRTSTMF = EXSTTMF),
    order = exprs(EXSTDTM, EXSEQ),
    mode = "first",
    by_vars = exprs(STUDYID, USUBJID)
  )

  saveRDS(adsl, file="/workflow/outputs/derived_adsl.rda")
