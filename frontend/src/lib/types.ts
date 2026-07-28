export interface SecurityIssue {
  severity: string;
  type: string;
  description: string;
  file: string;
}

export interface SecurityScan {
  semgrep_available: boolean;
  semgrep_reason: string;
  builtin_scan: boolean;
}

export interface TechStack {
  framework: string | null;
  language: string | null;
  database: string | null;
  ui_library: string | null;
  css_framework: string | null;
  authentication: string | null;
  packages: string[];
  dev_packages: string[];
}

export interface StaticAnalysis {
  total_files: number;
  total_lines: number;
  security_issues: SecurityIssue[];
  security_scan: SecurityScan;
  unused_packages: string[];
  missing_features: string[];
  redundant_features: string[];
  code_quality_score: number;
}

export interface LlmAnalysis {
  overall_score: number;
  code_quality: number;
  architecture: number;
  performance: number;
  security: number;
  summary: string;
  ai_mistakes: string[];
  recommendations: string[];
  roadmap: string[];
  prompt_generator: string;
}

export interface AnalysisResponse {
  project_id: string;
  tech_stack: TechStack;
  static_analysis: StaticAnalysis;
  llm_analysis: LlmAnalysis;
}

export interface ReportCategory {
  score: number;
  icon: string;
}

export interface Report {
  project_id: string;
  overall_score: number;
  categories: Record<string, ReportCategory>;
  tech_stack: TechStack;
  stats: {
    total_files: number;
    total_lines: number;
  };
  security_issues: SecurityIssue[];
  security_scan: SecurityScan;
  unused_packages: string[];
  missing_features: string[];
  redundant_features: string[];
  ai_mistakes: string[];
  recommendations: string[];
  roadmap: string[];
  summary: string;
  prompt_generator: string;
}

export interface UploadResult {
  project_id: string;
}
