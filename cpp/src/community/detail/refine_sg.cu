
#include <community/detail/refine.cuh>

namespace cugraph {
namespace detail {

template std::tuple<rmm::device_uvector<int32_t>,
                    std::pair<rmm::device_uvector<int32_t>, rmm::device_uvector<int32_t>>>
refine_clustering_2(
  raft::handle_t const& handle,
  cugraph::graph_view_t<int32_t, int32_t, float, false, false> const& graph_view,
  float total_edge_weight,
  float resolution,
  rmm::device_uvector<float> const& vertex_weights_v,
  rmm::device_uvector<int32_t>&& cluster_keys_v,
  rmm::device_uvector<float>&& cluster_weights_v,
  rmm::device_uvector<int32_t>&& next_clusters_v,
  edge_src_property_t<cugraph::graph_view_t<int32_t, int32_t, float, false, false>, float> const&
    src_vertex_weights_cache,
  edge_src_property_t<cugraph::graph_view_t<int32_t, int32_t, float, false, false>, int32_t> const&
    src_clusters_cache,
  edge_dst_property_t<cugraph::graph_view_t<int32_t, int32_t, float, false, false>, int32_t> const&
    dst_clusters_cache,
  bool up_down);

template std::tuple<rmm::device_uvector<int32_t>,
                    std::pair<rmm::device_uvector<int32_t>, rmm::device_uvector<int32_t>>>
refine_clustering_2(
  raft::handle_t const& handle,
  cugraph::graph_view_t<int32_t, int64_t, float, false, false> const& graph_view,
  float total_edge_weight,
  float resolution,
  rmm::device_uvector<float> const& vertex_weights_v,
  rmm::device_uvector<int32_t>&& cluster_keys_v,
  rmm::device_uvector<float>&& cluster_weights_v,
  rmm::device_uvector<int32_t>&& next_clusters_v,
  edge_src_property_t<cugraph::graph_view_t<int32_t, int64_t, float, false, false>, float> const&
    src_vertex_weights_cache,
  edge_src_property_t<cugraph::graph_view_t<int32_t, int64_t, float, false, false>, int32_t> const&
    src_clusters_cache,
  edge_dst_property_t<cugraph::graph_view_t<int32_t, int64_t, float, false, false>, int32_t> const&
    dst_clusters_cache,
  bool up_down);

template std::tuple<rmm::device_uvector<int64_t>,
                    std::pair<rmm::device_uvector<int64_t>, rmm::device_uvector<int64_t>>>
refine_clustering_2(
  raft::handle_t const& handle,
  cugraph::graph_view_t<int64_t, int64_t, float, false, false> const& graph_view,
  float total_edge_weight,
  float resolution,
  rmm::device_uvector<float> const& vertex_weights_v,
  rmm::device_uvector<int64_t>&& cluster_keys_v,
  rmm::device_uvector<float>&& cluster_weights_v,
  rmm::device_uvector<int64_t>&& next_clusters_v,
  edge_src_property_t<cugraph::graph_view_t<int64_t, int64_t, float, false, false>, float> const&
    src_vertex_weights_cache,
  edge_src_property_t<cugraph::graph_view_t<int64_t, int64_t, float, false, false>, int64_t> const&
    src_clusters_cache,
  edge_dst_property_t<cugraph::graph_view_t<int64_t, int64_t, float, false, false>, int64_t> const&
    dst_clusters_cache,
  bool up_down);

template std::tuple<rmm::device_uvector<int32_t>,
                    std::pair<rmm::device_uvector<int32_t>, rmm::device_uvector<int32_t>>>
refine_clustering_2(
  raft::handle_t const& handle,
  cugraph::graph_view_t<int32_t, int32_t, double, false, false> const& graph_view,
  double total_edge_weight,
  double resolution,
  rmm::device_uvector<double> const& vertex_weights_v,
  rmm::device_uvector<int32_t>&& cluster_keys_v,
  rmm::device_uvector<double>&& cluster_weights_v,
  rmm::device_uvector<int32_t>&& next_clusters_v,
  edge_src_property_t<cugraph::graph_view_t<int32_t, int32_t, double, false, false>, double> const&
    src_vertex_weights_cache,
  edge_src_property_t<cugraph::graph_view_t<int32_t, int32_t, double, false, false>, int32_t> const&
    src_clusters_cache,
  edge_dst_property_t<cugraph::graph_view_t<int32_t, int32_t, double, false, false>, int32_t> const&
    dst_clusters_cache,
  bool up_down);

template std::tuple<rmm::device_uvector<int32_t>,
                    std::pair<rmm::device_uvector<int32_t>, rmm::device_uvector<int32_t>>>
refine_clustering_2(
  raft::handle_t const& handle,
  cugraph::graph_view_t<int32_t, int64_t, double, false, false> const& graph_view,
  double total_edge_weight,
  double resolution,
  rmm::device_uvector<double> const& vertex_weights_v,
  rmm::device_uvector<int32_t>&& cluster_keys_v,
  rmm::device_uvector<double>&& cluster_weights_v,
  rmm::device_uvector<int32_t>&& next_clusters_v,
  edge_src_property_t<cugraph::graph_view_t<int32_t, int64_t, double, false, false>, double> const&
    src_vertex_weights_cache,
  edge_src_property_t<cugraph::graph_view_t<int32_t, int64_t, double, false, false>, int32_t> const&
    src_clusters_cache,
  edge_dst_property_t<cugraph::graph_view_t<int32_t, int64_t, double, false, false>, int32_t> const&
    dst_clusters_cache,
  bool up_down);

template std::tuple<rmm::device_uvector<int64_t>,
                    std::pair<rmm::device_uvector<int64_t>, rmm::device_uvector<int64_t>>>
refine_clustering_2(
  raft::handle_t const& handle,
  cugraph::graph_view_t<int64_t, int64_t, double, false, false> const& graph_view,
  double total_edge_weight,
  double resolution,
  rmm::device_uvector<double> const& vertex_weights_v,
  rmm::device_uvector<int64_t>&& cluster_keys_v,
  rmm::device_uvector<double>&& cluster_weights_v,
  rmm::device_uvector<int64_t>&& next_clusters_v,
  edge_src_property_t<cugraph::graph_view_t<int64_t, int64_t, double, false, false>, double> const&
    src_vertex_weights_cache,
  edge_src_property_t<cugraph::graph_view_t<int64_t, int64_t, double, false, false>, int64_t> const&
    src_clusters_cache,
  edge_dst_property_t<cugraph::graph_view_t<int64_t, int64_t, double, false, false>, int64_t> const&
    dst_clusters_cache,
  bool up_down);

}  // namespace detail
}  // namespace cugraph