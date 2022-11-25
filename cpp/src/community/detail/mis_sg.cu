#pragma once
#include <community/detail/mis_impl.cuh>

namespace cugraph {
namespace detail {
rmm::device_uvector<int32_t> compute_mis(
  raft::handle_t const& handle,
  graph_view_t<int32_t, int32_t, false, false> const& decision_graph_view,
  std::optional<edge_property_view_t<int32_t, float const*>> edge_weight_view);

rmm::device_uvector<int32_t> compute_mis(
  raft::handle_t const& handle,
  graph_view_t<int32_t, int32_t, false, false> const& decision_graph_view,
  std::optional<edge_property_view_t<int32_t, double const*>> edge_weight_view);

rmm::device_uvector<int32_t> compute_mis(
  raft::handle_t const& handle,
  graph_view_t<int32_t, int64_t, false, false> const& decision_graph_view,
  std::optional<edge_property_view_t<int64_t, float const*>> edge_weight_view);

rmm::device_uvector<int32_t> compute_mis(
  raft::handle_t const& handle,
  graph_view_t<int32_t, int64_t, false, false> const& decision_graph_view,
  std::optional<edge_property_view_t<int64_t, double const*>> edge_weight_view);

rmm::device_uvector<int64_t> compute_mis(
  raft::handle_t const& handle,
  graph_view_t<int64_t, int64_t, false, false> const& decision_graph_view,
  std::optional<edge_property_view_t<int64_t, float const*>> edge_weight_view);

rmm::device_uvector<int64_t> compute_mis(
  raft::handle_t const& handle,
  graph_view_t<int64_t, int64_t, false, false> const& decision_graph_view,
  std::optional<edge_property_view_t<int64_t, double const*>> edge_weight_view);

}  // namespace detail
}  // namespace cugraph