/*
 * Copyright (c) 2020-2021, NVIDIA CORPORATION.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#pragma once

#include <cugraph/algorithms.hpp>
#include <cugraph/graph_view.hpp>
#include <cugraph/utilities/error.hpp>

#include <raft/handle.hpp>

#include <cstddef>

namespace cugraph {

template <typename vertex_t, typename edge_t, typename weight_t, bool multi_gpu>
void core_number(raft::handle_t const& handle,
                 graph_view_t<vertex_t, edge_t, weight_t, false, multi_gpu> const& graph_view,
                 vertex_t* core_numbers,
                 k_core_degree_type_t degree_type,
                 size_t k_first,
                 size_t k_last,
                 bool do_expensive_check)
{
  CUGRAPH_FAIL("unimplemented.");
}

}  // namespace cugraph