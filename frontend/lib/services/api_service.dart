// This file handles communication with your FastAPI backend.

import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:frontend/models/project_input.dart';
import 'package:frontend/models/project_output.dart';

class ApiService {
  // Replace with your actual backend URL.
  // Make sure your FastAPI backend is running on this address.
  static const String _baseUrl = 'http://localhost:8000'; 

  Future<ProjectOutput> processProject(ProjectInput input) async {
    final url = Uri.parse('$_baseUrl/process_project');
    final headers = {'Content-Type': 'application/json'};
    final body = jsonEncode(input.toJson());

    try {
      final response = await http.post(url, headers: headers, body: body);

      if (response.statusCode == 200) {
        final Map<String, dynamic> jsonResponse = jsonDecode(response.body);
        return ProjectOutput.fromJson(jsonResponse);
      } else {
        // Handle non-200 status codes
        print('Backend error: ${response.statusCode} - ${response.body}');
        throw Exception('Failed to process project: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      // Handle network errors or other exceptions
      print('Error sending request: $e');
      throw Exception('Failed to connect to backend: $e');
    }
  }
}