"""
Photonic Computing Web Application
Interactive demonstration of photonic computing capabilities
"""

from flask import Flask, render_template, jsonify, request
import numpy as np
import json
from photonic_core import (
    PhotonicMatrixMultiplier, WDMMultiplexer, PhotonicFFT,
    calculate_photonic_performance
)
from pcie_interface import PhotonicPCIeBoard, MultiboardCluster
from fpga_integration import HybridFPGAPhotonic, LargeScaleComputeCluster

app = Flask(__name__)

# Initialize photonic components
matrix_multiplier = PhotonicMatrixMultiplier(size=128)
wdm_system = WDMMultiplexer(num_channels=64)
fft_processor = PhotonicFFT(size=1024)
pcie_board = PhotonicPCIeBoard()
hybrid_system = HybridFPGAPhotonic()

# Initialize board
pcie_board.initialize()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/performance')
def get_performance():
    """Get overall system performance metrics"""
    perf = calculate_photonic_performance(matrix_size=1024, num_wdm_channels=64)
    
    return jsonify({
        'matrix_multiply_tops': perf['matrix_multiply_tops'],
        'total_throughput_tops': perf['total_throughput_tops'],
        'aggregate_bandwidth_tbps': perf['aggregate_bandwidth_tbps'],
        'fft_latency_ns': perf['fft_latency_ns'],
        'energy_efficiency_tops_per_watt': perf['energy_efficiency_tops_per_watt'],
        'speedup_vs_electronic': perf['speedup_vs_electronic']
    })

@app.route('/api/matrix_multiply', methods=['POST'])
def matrix_multiply():
    """Execute matrix multiplication"""
    data = request.json
    size = data.get('size', 128)
    
    # Create random test vector
    vector = np.random.randn(size) + 1j * np.random.randn(size)
    
    # Perform multiplication
    result = matrix_multiplier.multiply(vector)
    throughput = matrix_multiplier.compute_throughput()
    
    return jsonify({
        'size': size,
        'throughput_tops': throughput,
        'latency_ns': 10.0,
        'result_magnitude': float(np.abs(result).mean()),
        'energy_pj': 0.1
    })

@app.route('/api/wdm_channels')
def get_wdm_channels():
    """Get WDM channel information"""
    wavelengths = wdm_system.resonance_wavelengths(center=1550.0, num=64)
    bandwidth = wdm_system.aggregate_bandwidth()
    
    return jsonify({
        'num_channels': wdm_system.num_channels,
        'wavelengths': wavelengths.tolist(),
        'channel_spacing_nm': wdm_system.channel_spacing,
        'aggregate_bandwidth_tbps': bandwidth,
        'per_channel_gbps': 100.0
    })

@app.route('/api/fft', methods=['POST'])
def compute_fft():
    """Compute photonic FFT"""
    data = request.json
    size = data.get('size', 1024)
    
    # Create test data
    test_data = np.random.randn(size) + 1j * np.random.randn(size)
    
    # Compute FFT
    result = fft_processor.compute(test_data)
    latency = fft_processor.latency_ns()
    
    return jsonify({
        'size': size,
        'latency_ns': latency,
        'speedup_vs_electronic': 1000.0,
        'result_magnitude': float(np.abs(result).mean())
    })

@app.route('/api/pcie_board')
def get_pcie_board_info():
    """Get PCIe board information"""
    info = pcie_board.get_board_info()
    
    return jsonify({
        'pcie_generation': info['pcie_generation'],
        'pcie_lanes': info['pcie_lanes'],
        'pcie_bandwidth_gbps': info['pcie_bandwidth_gbps'],
        'form_factor': info['form_factor'],
        'power_consumption_w': info['power_consumption_w'],
        'num_optical_ports': info['num_optical_ports'],
        'num_lasers': info['num_lasers'],
        'num_modulators': info['num_modulators'],
        'matrix_size': info['matrix_size']
    })

@app.route('/api/pcie_transfer', methods=['POST'])
def pcie_transfer():
    """Simulate PCIe data transfer"""
    data = request.json
    size = data.get('size', 1024)
    
    # Create test matrix
    matrix = np.random.randn(size, size).astype(np.float32)
    
    # Transfer to device
    transfer_time = pcie_board.transfer_matrix_to_device(matrix)
    
    return jsonify({
        'matrix_size': size,
        'transfer_time_ms': transfer_time,
        'data_size_mb': (matrix.nbytes / 1e6),
        'transfer_rate_gbps': (matrix.nbytes * 8) / (transfer_time / 1000) / 1e9
    })

@app.route('/api/hybrid_system')
def get_hybrid_system():
    """Get hybrid FPGA-photonic system specs"""
    specs = hybrid_system.get_system_specs()
    
    return jsonify({
        'fpga': specs['fpga'],
        'photonic': specs['photonic'],
        'optical_io': specs['optical_io'],
        'memory': specs['memory']
    })

@app.route('/api/execute_workload', methods=['POST'])
def execute_workload():
    """Execute workload on hybrid system"""
    data = request.json
    size = data.get('size', 1024)
    
    result = hybrid_system.execute_matrix_multiply(size)
    
    return jsonify({
        'size': result['size'],
        'fpga_time_ms': result['fpga_time_ms'],
        'photonic_time_ns': result['photonic_time_ns'],
        'transfer_time_ms': result['transfer_time_ms'],
        'total_time_ms': result['total_time_ms'],
        'throughput_tflops': result['throughput_tflops'],
        'partition': result['partition']
    })

@app.route('/api/cluster')
def get_cluster_info():
    """Get cluster information"""
    cluster = LargeScaleComputeCluster(num_nodes=64)
    perf = cluster.aggregate_performance()
    
    return jsonify({
        'num_nodes': perf['num_nodes'],
        'total_pflops': perf['total_pflops'],
        'total_power_kw': perf['total_power_kw'],
        'efficiency_gflops_per_watt': perf['efficiency_gflops_per_watt'],
        'total_memory_tb': perf['total_memory_tb'],
        'optical_fabric_pbps': perf['optical_fabric_pbps'],
        'network_topology': perf['network_topology']
    })

if __name__ == '__main__':
    print("=" * 70)
    print("PHOTONIC COMPUTING WEB APPLICATION")
    print("=" * 70)
    print("\nInitializing photonic components...")
    print(f"  Matrix Multiplier: {matrix_multiplier.size}x{matrix_multiplier.size}")
    print(f"  WDM Channels: {wdm_system.num_channels}")
    print(f"  FFT Size: {fft_processor.size}")
    print(f"  PCIe Board: {pcie_board.pcie.generation.value[1]} x{pcie_board.pcie.num_lanes}")
    print("\n" + "=" * 70)
    print("Starting server on http://127.0.0.1:5001")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=5001, debug=False)
