// This is the main UI screen where users interact with the system.

import 'package:flutter/material.dart';
import 'package:frontend/models/project_input.dart';
import 'package:frontend/models/project_output.dart';
import 'package:frontend/services/api_service.dart';
import 'dart:convert'; // For base64 decoding

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _formKey = GlobalKey<FormState>();
  final ApiService _apiService = ApiService();

  // Text editing controllers for form fields
  final TextEditingController _projectTypeController = TextEditingController(text: 'residential');
  final TextEditingController _clientNameController = TextEditingController(text: 'EcoHome Developers');
  final TextEditingController _budgetRangeController = TextEditingController(text: '\$750,000 - \$1,200,000');
  final TextEditingController _locationController = TextEditingController(text: 'London, UK');
  final TextEditingController _desiredFeaturesController = TextEditingController(text: 'Smart Home Tech, Green Roof, Open Concept Living');
  final TextEditingController _initialIdeasUrlController = TextEditingController(text: '[https://example.com/eco-home-ideas](https://example.com/eco-home-ideas)');
  final TextEditingController _projectDescriptionController = TextEditingController(text: 'Design and build a two-story modern eco-friendly family house with smart home technology, a green roof, and an emphasis on energy efficiency and natural light.');
  final TextEditingController _projectSizeController = TextEditingController(text: 'medium');

  ProjectOutput? _projectOutput;
  bool _isLoading = false;
  String? _errorMessage;

  Future<void> _processProject() async {
    if (_formKey.currentState!.validate()) {
      setState(() {
        _isLoading = true;
        _errorMessage = null;
        _projectOutput = null;
      });

      final projectInput = ProjectInput(
        projectType: _projectTypeController.text,
        clientName: _clientNameController.text,
        budgetRange: _budgetRangeController.text,
        location: _locationController.text,
        desiredFeatures: _desiredFeaturesController.text.split(',').map((s) => s.trim()).where((s) => s.isNotEmpty).toList(),
        initialIdeasUrl: _initialIdeasUrlController.text.isEmpty ? null : _initialIdeasUrlController.text,
        projectDescription: _projectDescriptionController.text,
        projectSize: _projectSizeController.text,
      );

      try {
        final output = await _apiService.processProject(projectInput);
        setState(() {
          _projectOutput = output;
        });
      } catch (e) {
        setState(() {
          _errorMessage = e.toString();
        });
      } finally {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  void dispose() {
    _projectTypeController.dispose();
    _clientNameController.dispose();
    _budgetRangeController.dispose();
    _locationController.dispose();
    _desiredFeaturesController.dispose();
    _initialIdeasUrlController.dispose();
    _projectDescriptionController.dispose();
    _projectSizeController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Construction AI Assistant'),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Form(
                  key: _formKey,
                  child: Column(
                    children: [
                      Text('Enter Project Details', style: Theme.of(context).textTheme.headlineMedium),
                      const SizedBox(height: 20),
                      _buildTextField(_projectDescriptionController, 'Project Description', maxLines: 3),
                      _buildTextField(_projectTypeController, 'Project Type (e.g., residential, commercial)'),
                      _buildTextField(_clientNameController, 'Client Name'),
                      _buildTextField(_budgetRangeController, 'Budget Range (e.g., \$750,000 - \$1,200,000)'),
                      _buildTextField(_locationController, 'Location (e.g., London, UK)'),
                      _buildTextField(_desiredFeaturesController, 'Desired Features (comma-separated)', hintText: 'e.g., Smart Home, Green Roof'),
                      _buildTextField(_initialIdeasUrlController, 'Initial Ideas URL (Optional)'),
                      _buildTextField(_projectSizeController, 'Project Size (e.g., small, medium, large)'),
                      const SizedBox(height: 20),
                      _isLoading
                          ? const CircularProgressIndicator()
                          : ElevatedButton(
                              onPressed: _processProject,
                              child: const Text('Get AI Analysis'),
                            ),
                      if (_errorMessage != null)
                        Padding(
                          padding: const EdgeInsets.only(top: 16.0),
                          child: Text(
                            'Error: $_errorMessage',
                            style: const TextStyle(color: Colors.red),
                            textAlign: TextAlign.center,
                          ),
                        ),
                    ],
                  ),
                ),
              ),
            ),
            const SizedBox(height: 20),
            if (_projectOutput != null)
              _buildOutputDisplay(_projectOutput!),
          ],
        ),
      ),
    );
  }

  Widget _buildTextField(TextEditingController controller, String label, {int maxLines = 1, String? hintText}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: TextFormField(
        controller: controller,
        decoration: InputDecoration(
          labelText: label,
          hintText: hintText,
        ),
        maxLines: maxLines,
        validator: (value) {
          if (label.contains('Optional')) return null;
          if (value == null || value.isEmpty) {
            return 'Please enter $label';
          }
          return null;
        },
      ),
    );
  }

  Widget _buildOutputDisplay(ProjectOutput output) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('AI Analysis Results', style: Theme.of(context).textTheme.headlineMedium),
            const SizedBox(height: 10),
            _buildResultRow('Overall Status:', output.overallStatus, color: _getStatusColor(output.overallStatus)),
            _buildResultRow('Summary Message:', output.summaryMessage),
            const SizedBox(height: 20),
            Text('Consolidated Project Data:', style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 10),
            _buildConsolidatedDataDisplay(output.consolidatedProjectData),
            const SizedBox(height: 20),
            Text('Raw Agent Outputs (for debugging):', style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 10),
            _buildRawAgentOutputsDisplay(output.agentOutputsRaw),
          ],
        ),
      ),
    );
  }

  Widget _buildResultRow(String label, String value, {Color? color}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label, style: const TextStyle(fontWeight: FontWeight.bold)),
          const SizedBox(width: 8),
          Expanded(
            child: Text(value, style: TextStyle(color: color ?? Colors.black87)),
          ),
        ],
      ),
    );
  }

  Color _getStatusColor(String status) {
    switch (status.toLowerCase()) {
      case 'success':
        return Colors.green.shade700;
      case 'partial_success':
        return Colors.orange.shade700;
      case 'failure':
        return Colors.red.shade700;
      default:
        return Colors.black87;
    }
  }

  Widget _buildConsolidatedDataDisplay(Map<String, dynamic> data) {
    return Column(
      children: data.entries.map((entry) {
        // Special handling for image data
        if (entry.key == 'digital_twin_output' && entry.value is Map<String, dynamic>) {
          final digitalTwinOutput = entry.value as Map<String, dynamic>;
          return ExpansionTile(
            title: Text('Digital Twin Output', style: Theme.of(context).textTheme.titleMedium),
            children: [
              _buildImageDisplay('Exterior Render', digitalTwinOutput['full_exterior_render_base64']),
              _buildImageDisplay('Interior Render', digitalTwinOutput['full_interior_render_base64']),
              _buildKeyValueDisplay(digitalTwinOutput),
            ],
          );
        } else if (entry.value is Map<String, dynamic>) {
          // For other nested JSON objects
          return ExpansionTile(
            title: Text(_formatKey(entry.key), style: Theme.of(context).textTheme.titleMedium),
            children: [
              _buildKeyValueDisplay(entry.value as Map<String, dynamic>),
            ],
          );
        } else if (entry.value is List) {
          // For lists
          return ExpansionTile(
            title: Text(_formatKey(entry.key), style: Theme.of(context).textTheme.titleMedium),
            children: [
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: (entry.value as List).map((item) => Text('- ${item.toString()}')).toList(),
                ),
              ),
            ],
          );
        } else {
          // For simple key-value pairs
          return _buildResultRow(_formatKey(entry.key) + ':', entry.value.toString());
        }
      }).toList(),
    );
  }

  Widget _buildKeyValueDisplay(Map<String, dynamic> data) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: data.entries.map((itemEntry) {
          if (itemEntry.key.contains('_base64') && itemEntry.value is String) {
            // Skip full base64 string display here, handled by _buildImageDisplay
            return const SizedBox.shrink();
          }
          return Text('${_formatKey(itemEntry.key)}: ${itemEntry.value.toString()}');
        }).toList(),
      ),
    );
  }

  Widget _buildImageDisplay(String title, String? base64String) {
    if (base64String == null || base64String.isEmpty || base64String == 'N/A') {
      return Padding(
        padding: const EdgeInsets.symmetric(vertical: 8.0),
        child: Text('$title: No image generated or available.', style: const TextStyle(fontStyle: FontStyle.italic)),
      );
    }
    try {
      final bytes = base64Decode(base64String);
      return Padding(
        padding: const EdgeInsets.symmetric(vertical: 8.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Image.memory(bytes, fit: BoxFit.contain, errorBuilder: (context, error, stackTrace) {
              return Text('Failed to load image for $title: $error');
            }),
          ],
        ),
      );
    } catch (e) {
      return Padding(
        padding: const EdgeInsets.symmetric(vertical: 8.0),
        child: Text('Error decoding image for $title: $e', style: const TextStyle(color: Colors.red)),
      );
    }
  }

  Widget _buildRawAgentOutputsDisplay(Map<String, dynamic> data) {
    return Column(
      children: data.entries.map((entry) {
        return ExpansionTile(
          title: Text(_formatKey(entry.key), style: Theme.of(context).textTheme.titleMedium),
          children: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
              child: Text(jsonEncode(entry.value)), // Display raw JSON for debugging
            ),
          ],
        );
      }).toList(),
    );
  }

  String _formatKey(String key) {
    return key.replaceAll('_', ' ').split(' ').map((word) => word[0].toUpperCase() + word.substring(1)).join(' ');
  }
}
