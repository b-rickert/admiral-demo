from flytekit import workflow
from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import FlyteFile
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask, DatasetSnapshot
from flytekitplugins.domino.helpers import Input, Output, run_domino_job_task
from typing import TypeVar, NamedTuple, List
import flytekit
from pathlib import Path

class FinalOutputs(NamedTuple):
    derived_adsl: FlyteFile

@workflow
def simple_admiral_workflow() -> FinalOutputs:

    #Flows requires the user to take a snapshot of a Dataset, presumably for read-only purposes. You can find the ID of your snapshot using the Domino API.
    snapshot = DatasetSnapshot(Name='Admiral-Demo-Git', Id='69a1b3943587c61f32cedf29', Version=1)

    #Using the Domino helpers Input object type for simplicity, we define our job1 Input filepath strings as a list.
    inputDatasets = [
        Input(name="ex", type=str, value="/mnt/data/Admiral-Demo/ex.rda"),
        Input(name="vs", type=str, value="/mnt/data/Admiral-Demo/vs.rda"),
        Input(name="admiral_adsl", type=str, value="/mnt/data/Admiral-Demo/admiral_adsl.rda")
    ]

    #Similar to the inputs, we define our outputs as a list FlyteFiles because the outputs are pushed to the flyte blob storage account in Azure
    #To learn more about FlyteFiles, see the docs at https://docs.flyte.org/en/latest/user_guide/data_types_and_io/flytefile.html
    formatedDatasets = [
        Output(name="ex_ext", type=FlyteFile),
        Output(name="vs", type=FlyteFile),
        Output(name="adsl", type=FlyteFile)
    ]

    # Start first job to load and format the ADaM Datasets using the method from domino helpers. Note that the command is similar to a typical Domino Job
    formatDatasets = run_domino_job_task("Format Datasets", command="Rscript /mnt/code/domino-scripts/admiralFlow/loadDatasets.r", environment_name="Admiral",  output_specs=formatedDatasets, inputs=inputDatasets, dataset_snapshots=[snapshot], use_project_defaults_for_omitted=True)
   
    
 #Create second task
    derivedVars = [
        Output(name="derived_adsl", type=FlyteFile)
    ]
    deriveVarsInputs = [
        Input(name="adsl", type=FlyteFile, value=formatDatasets[2]), 
        Input(name="ex_ext", type=FlyteFile, value=formatDatasets[0])
        ]
    deriveVars = run_domino_job_task("Derive Variables", command="Rscript /mnt/code/domino-scripts/admiralFlow/deriveDatasets.r", environment_name="Admiral", inputs=deriveVarsInputs, output_specs=derivedVars, use_project_defaults_for_omitted=True)

    return FinalOutputs(derived_adsl=deriveVars[0])
