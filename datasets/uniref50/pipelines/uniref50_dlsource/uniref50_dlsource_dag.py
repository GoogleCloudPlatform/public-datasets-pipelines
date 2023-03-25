# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from airflow import DAG
from airflow.operators import bash

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2022-06-10",
}


with DAG(
    dag_id="uniref50.uniref50_download_source",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to copy `uniref50.fasta` to gcs
    download_zip_file = bash.BashOperator(
        task_id="download_zip_file",
        bash_command='# mkdir -p $data_dir/uniref\n# curl -o $data_dir/uniref/uniref50.fasta.gz -L $uniref50\n# apt-get -y update \u0026\u0026 apt-get install -y pigz\ngunzip -c $data_dir/uniref/uniref50.fasta.gz |sed \u0027s/:\u003e/|/g\u0027 |sed \u0027s/ TaxID=/|Size=/g\u0027 |sed \u0027s/\u003e\\(UniRef50_[^[:space:]]*[[:space:]]\\)/ClusterID=\\1|TaxID=/;s/ |/|/\u0027 |sed \u0027s/ RepID=/|ClusterName=/g\u0027 |sed \u0027s/ Tax=/|Sequence=/g\u0027 |sed \u0027s/ n=/|RepID=/g\u0027 |sed \u0027s/ClusterID=//g\u0027 |sed \u0027s/TaxID=//g\u0027 |sed \u0027s/RepID=//g\u0027 |sed \u0027s/Sequence=//g\u0027 |sed \u0027s/Size=//g\u0027 |sed \u0027s/ClusterName=//g\u0027 |sed \u0027/^UniRef50_/ s/$/|ENDOFHEADERROW/\u0027 |sed \u0027/|ENDOFHEADERROW/! s/$/-/\u0027 |perl -p -e \u0027s/-\\n/-/g\u0027 |sed \u0027s/\\-UniRef/-\\nUniRef/g\u0027 |perl -p -e \u0027s/\\|ENDOFHEADERROW\\n/|/g\u0027 |sed \u0027s/-$//g\u0027 | split -a 3 -d -l 2000000 --numeric-suffixes --filter=\u0027gzip -9 \u003e $data_dir/uniref/$FILE.txt.gz\u0027\n# gunzip -fv $data_dir/uniref/uniref50.fasta.gz\n# awk \u0027BEGIN {n_seq=0;} /^\u003e/ {if(n_seq%10000000==0){file=sprintf("/home/airflow/gcs/data/uniref50/uniref/myseq%d.fa",n_seq);}\n# print \u003e\u003e file; n_seq++; next;} { print \u003e\u003e file; }\u0027 \u003c $data_dir/uniref/uniref50.fasta\n# awk \u0027BEGIN {n_seq=0;} /^\u003e/ {if(n_seq%3500000==0){file=sprintf("/home/airflow/gcs/data/uniref50/uniref/myseq_1%d.fa",n_seq);}\n# print \u003e\u003e file; n_seq++; next;} { print \u003e\u003e file; }\u0027 \u003c $data_dir/uniref/myseq0.fa\n# rm $data_dir/uniref/uniref50.fasta.gz\n# rm $data_dir/uniref/uniref50.fasta\n# rm $data_dir/uniref/myseq0.fa\n',
        env={
            "data_dir": "/home/airflow/gcs/data/uniref50",
            "uniref50": "https://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref50/uniref50.fasta.gz",
        },
    )

    download_zip_file
