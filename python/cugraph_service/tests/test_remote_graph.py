# Copyright (c) 2022, NVIDIA CORPORATION.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import subprocess
import random
import time


import pytest

from . import data

import cudf

from cugraph.experimental import PropertyGraph
from cugraph_service_client import RemotePropertyGraph

###############################################################################
# fixtures


@pytest.fixture(scope="module")
def server(graph_creation_extension1):
    """
    Start a cugraph_service server, stop it when done with the fixture.  This
    also uses graph_creation_extension1 to preload a graph creation extension.
    """
    from cugraph_service_server import server
    from cugraph_service_client import CugraphServiceClient
    from cugraph_service_client.exceptions import CugraphServiceError

    server_file = server.__file__
    server_process = None
    host = "localhost"
    port = 9090
    graph_creation_extension_dir = graph_creation_extension1
    client = CugraphServiceClient(host, port)

    try:
        client.uptime()
        print("FOUND RUNNING SERVER, ASSUMING IT SHOULD BE USED FOR TESTING!")
        yield

    except CugraphServiceError:
        # A server was not found, so start one for testing then stop it when
        # testing is done.

        # pytest will update sys.path based on the tests it discovers, and for
        # this source tree, an entry for the parent of this "tests" directory
        # will be added. The parent to this "tests" directory also allows
        # imports to find the cugraph_service sources, so in oder to ensure the
        # server that's started is also using the same sources, the PYTHONPATH
        # env should be set to the sys.path being used in this process.
        env_dict = os.environ.copy()
        env_dict["PYTHONPATH"] = ":".join(sys.path)

        with subprocess.Popen(
            [
                sys.executable,
                server_file,
                "--host",
                host,
                "--port",
                str(port),
                "--graph-creation-extension-dir",
                graph_creation_extension_dir,
            ],
            env=env_dict,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        ) as server_process:
            try:
                print(
                    "\nLaunched cugraph_service server, waiting for it to " "start...",
                    end="",
                    flush=True,
                )
                max_retries = 10
                retries = 0
                while retries < max_retries:
                    try:
                        client.uptime()
                        print("started.")
                        break
                    except CugraphServiceError:
                        time.sleep(1)
                        retries += 1
                if retries >= max_retries:
                    raise RuntimeError("error starting server")
            except Exception:
                if server_process.poll() is None:
                    server_process.terminate()
                raise

            # yield control to the tests
            yield

            # tests are done, now stop the server
            print("\nTerminating server...", end="", flush=True)
            server_process.terminate()
            print("done.", flush=True)


@pytest.fixture(scope="function")
def client(server):
    """
    Creates a client instance to the running server, closes the client when the
    fixture is no longer used by tests.
    """
    from cugraph_service_client import CugraphServiceClient, defaults

    client = CugraphServiceClient(defaults.host, defaults.port)

    for gid in client.get_graph_ids():
        client.delete_graph(gid)

    # FIXME: should this fixture always unconditionally unload all extensions?
    # client.unload_graph_creation_extensions()

    # yield control to the tests
    yield client

    # tests are done, now stop the server
    client.close()


@pytest.fixture(scope="function")
def client_with_property_csvs_loaded(client):
    """
    Loads each of the vertex and edge property CSVs into the default graph on
    the server.
    """
    merchants = data.property_csv_data["merchants"]
    users = data.property_csv_data["users"]
    transactions = data.property_csv_data["transactions"]
    relationships = data.property_csv_data["relationships"]
    referrals = data.property_csv_data["referrals"]

    client.load_csv_as_vertex_data(
        merchants["csv_file_name"],
        dtypes=merchants["dtypes"],
        vertex_col_name=merchants["vert_col_name"],
        header=0,
        type_name="merchants",
    )
    client.load_csv_as_vertex_data(
        users["csv_file_name"],
        dtypes=users["dtypes"],
        vertex_col_name=users["vert_col_name"],
        header=0,
        type_name="users",
    )

    client.load_csv_as_edge_data(
        transactions["csv_file_name"],
        dtypes=transactions["dtypes"],
        vertex_col_names=transactions["vert_col_names"],
        header=0,
        type_name="transactions",
    )
    client.load_csv_as_edge_data(
        relationships["csv_file_name"],
        dtypes=relationships["dtypes"],
        vertex_col_names=relationships["vert_col_names"],
        header=0,
        type_name="relationships",
    )
    client.load_csv_as_edge_data(
        referrals["csv_file_name"],
        dtypes=referrals["dtypes"],
        vertex_col_names=referrals["vert_col_names"],
        header=0,
        type_name="referrals",
    )

    assert client.get_graph_ids() == [0]
    return client


@pytest.fixture(scope="function")
def pG_with_property_csvs_loaded():
    """
    Loads each of the vertex and edge property CSVs into a
    property graph.
    """
    pG = PropertyGraph()
    merchants = data.property_csv_data["merchants"]
    users = data.property_csv_data["users"]
    transactions = data.property_csv_data["transactions"]
    relationships = data.property_csv_data["relationships"]
    referrals = data.property_csv_data["referrals"]

    merchants_df = cudf.read_csv(
        merchants["csv_file_name"], dtype=merchants["dtypes"], header=0, delimiter=" "
    )
    pG.add_vertex_data(
        merchants_df,
        vertex_col_name=merchants["vert_col_name"],
        type_name="merchants",
    )

    users_df = cudf.read_csv(
        users["csv_file_name"], dtype=users["dtypes"], header=0, delimiter=" "
    )
    pG.add_vertex_data(
        users_df,
        vertex_col_name=users["vert_col_name"],
        type_name="users",
    )

    transactions_df = cudf.read_csv(
        transactions["csv_file_name"],
        dtype=transactions["dtypes"],
        header=0,
        delimiter=" ",
    )
    pG.add_edge_data(
        transactions_df,
        vertex_col_names=transactions["vert_col_names"],
        type_name="transactions",
    )

    relationships_df = cudf.read_csv(
        relationships["csv_file_name"],
        dtype=relationships["dtypes"],
        header=0,
        delimiter=" ",
    )
    pG.add_edge_data(
        relationships_df,
        vertex_col_names=relationships["vert_col_names"],
        type_name="relationships",
    )

    referrals_df = cudf.read_csv(
        referrals["csv_file_name"], dtype=referrals["dtypes"], header=0, delimiter=" "
    )
    pG.add_edge_data(
        referrals_df,
        vertex_col_names=referrals["vert_col_names"],
        type_name="referrals",
    )
    return pG


def test_graph_info(client_with_property_csvs_loaded, pG_with_property_csvs_loaded):
    rpG = RemotePropertyGraph(client_with_property_csvs_loaded, 0)
    pG = pG_with_property_csvs_loaded
    graph_info = rpG.graph_info

    expected_results = {
        "num_edges": pG.get_num_edges(),
        "num_edge_properties": len(pG.edge_property_names),
        "num_vertices": pG.get_num_vertices(),
        "num_vertex_properties": len(pG.vertex_property_names),
        "num_vertices_from_vertex_data": pG.get_num_vertices(include_edge_data=False),
    }

    assert set(graph_info.keys()) == set(expected_results.keys())
    for k in expected_results:
        assert graph_info[k] == expected_results[k]


def test_edges(client_with_property_csvs_loaded, pG_with_property_csvs_loaded):
    # FIXME update this when edges() method issue is resolved.
    rpG = RemotePropertyGraph(client_with_property_csvs_loaded, 0)
    pG = pG_with_property_csvs_loaded

    edges = pG.get_edge_data(
        columns=[pG.src_col_name, pG.dst_col_name, pG.type_col_name]
    )
    rpG_edges = rpG.edges

    assert (edges[pG.edge_id_col_name] == rpG_edges[rpG.edge_id_col_name]).all()
    assert (edges[pG.src_col_name] == rpG_edges[rpG.src_col_name]).all()
    assert (edges[pG.dst_col_name] == rpG_edges[rpG.dst_col_name]).all()
    assert (
        edges[pG.type_col_name].astype("string")
        == rpG_edges[rpG.type_col_name].astype("string")
    ).all()


def test_property_type_names(
    client_with_property_csvs_loaded, pG_with_property_csvs_loaded
):
    rpG = RemotePropertyGraph(client_with_property_csvs_loaded, 0)
    pG = pG_with_property_csvs_loaded

    assert rpG.vertex_property_names == pG.vertex_property_names
    assert rpG.edge_property_names == pG.edge_property_names
    assert rpG.vertex_types == pG.vertex_types
    assert rpG.edge_types == pG.edge_types


def test_num_elements(client_with_property_csvs_loaded, pG_with_property_csvs_loaded):
    rpG = RemotePropertyGraph(client_with_property_csvs_loaded, 0)
    pG = pG_with_property_csvs_loaded

    assert rpG.get_num_vertices() == pG.get_num_vertices()
    assert rpG.get_num_vertices(include_edge_data=False) == pG.get_num_vertices(
        include_edge_data=False
    )
    for type in pG.vertex_types:
        assert rpG.get_num_vertices(type=type) == pG.get_num_vertices(type=type)
        assert rpG.get_num_vertices(
            type=type, include_edge_data=False
        ) == pG.get_num_vertices(type=type, include_edge_data=False)

    assert rpG.get_num_edges() == pG.get_num_edges()
    for type in pG.edge_types:
        assert rpG.get_num_edges(type=type) == pG.get_num_edges(type=type)


def test_get_vertex_data(
    client_with_property_csvs_loaded, pG_with_property_csvs_loaded
):
    rpG = RemotePropertyGraph(client_with_property_csvs_loaded, 0)
    pG = pG_with_property_csvs_loaded

    vd = rpG.get_vertex_data()
    vd[rpG.type_col_name] = vd[rpG.type_col_name].astype("string")
    expected_vd = pG.get_vertex_data().fillna(0)  # FIXME expose na handling
    expected_vd[pG.type_col_name] = expected_vd[pG.type_col_name].astype("string")
    for col in expected_vd.columns:
        assert (expected_vd[col] == vd[col]).all()

    for _ in range(3):
        vertex_ids = random.sample(pG.vertices_ids().values_host.tolist(), 3)
        vd = rpG.get_vertex_data(vertex_ids=vertex_ids)
        vd[rpG.type_col_name] = vd[rpG.type_col_name].astype("string")
        expected_vd = pG.get_vertex_data(vertex_ids=vertex_ids).fillna(
            0
        )  # FIXME expose na handling
        expected_vd[pG.type_col_name] = expected_vd[pG.type_col_name].astype("string")
        for col in expected_vd.columns:
            assert (expected_vd[col] == vd[col]).all()

    vertex_type_list = [["merchants", "users"], ["merchants"]]
    for vertex_types in vertex_type_list:
        vd = rpG.get_vertex_data(types=vertex_types)
        vd[rpG.type_col_name] = vd[rpG.type_col_name].astype("string")
        expected_vd = pG.get_vertex_data(types=vertex_types).fillna(
            0
        )  # FIXME expose na handling
        expected_vd[pG.type_col_name] = expected_vd[pG.type_col_name].astype("string")
        for col in expected_vd.columns:
            assert (expected_vd[col] == vd[col]).all()

    vd = rpG.get_vertex_data(types=["users"], columns=["vertical"])
    vd[rpG.type_col_name] = vd[rpG.type_col_name].astype("string")
    expected_vd = pG.get_vertex_data(types=["users"], columns=["vertical"]).fillna(
        0
    )  # FIXME expose na handling
    expected_vd[pG.type_col_name] = expected_vd[pG.type_col_name].astype("string")
    for col in expected_vd.columns:
        assert (expected_vd[col] == vd[col]).all()


def test_get_edge_data(client_with_property_csvs_loaded, pG_with_property_csvs_loaded):
    rpG = RemotePropertyGraph(client_with_property_csvs_loaded, 0)
    pG = pG_with_property_csvs_loaded

    ed = rpG.get_edge_data()
    ed[rpG.type_col_name] = ed[rpG.type_col_name].astype("string")
    expected_ed = pG.get_edge_data().fillna(0)  # FIXME expose na handling
    expected_ed[pG.type_col_name] = expected_ed[pG.type_col_name].astype("string")
    for col in expected_ed.columns:
        assert (expected_ed[col] == ed[col]).all()

    for _ in range(3):
        edge_ids = random.sample(
            pG.get_edge_data()[pG.edge_id_col_name].values_host.tolist(), 3
        )
        ed = rpG.get_edge_data(edge_ids=edge_ids)
        ed[rpG.type_col_name] = ed[rpG.type_col_name].astype("string")
        expected_ed = pG.get_edge_data(edge_ids=edge_ids).fillna(
            0
        )  # FIXME expose na handling
        expected_ed[pG.type_col_name] = expected_ed[pG.type_col_name].astype("string")
        for col in expected_ed.columns:
            assert (expected_ed[col] == ed[col]).all()

    for edge_types in [["transactions", "relationships"], ["referrals"]]:
        ed = rpG.get_edge_data(types=edge_types)
        ed[rpG.type_col_name] = ed[rpG.type_col_name].astype("string")
        expected_ed = pG.get_edge_data(types=edge_types).fillna(
            0
        )  # FIXME expose na handling
        expected_ed[pG.type_col_name] = expected_ed[pG.type_col_name].astype("string")
        for col in expected_ed.columns:
            assert (expected_ed[col] == ed[col]).all()

    ed = rpG.get_edge_data(types=["referrals"], columns=["stars", "merchant_id"])
    ed[rpG.type_col_name] = ed[rpG.type_col_name].astype("string")
    expected_ed = pG.get_edge_data(
        types=["referrals"], columns=["stars", "merchant_id"]
    ).fillna(
        0
    )  # FIXME expose na handling
    expected_ed[pG.type_col_name] = expected_ed[pG.type_col_name].astype("string")
    for col in expected_ed.columns:
        assert (expected_ed[col] == ed[col]).all()


@pytest.mark.skip(reason="not yet implemented")
def test_add_vertex_data(
    client_with_property_csvs_loaded, pG_with_property_csvs_loaded
):
    raise NotImplementedError()


@pytest.mark.skip(reason="not yet implemented")
def test_add_edge_data(client_with_property_csvs_loaded, pG_with_property_csvs_loaded):

    raise NotImplementedError()
