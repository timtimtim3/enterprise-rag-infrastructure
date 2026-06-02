import type { MessageSourceInfo, Source } from "../../types/api";
import { FileText, Globe, Database, File } from "lucide-react";

type SourceCardProps = {
  source: MessageSourceInfo | Source;
  index: number;
};

function getSourceIcon(sourceType: string) {
  switch (sourceType.toLowerCase()) {
    case "web":
    case "url":
      return Globe;
    case "database":
    case "db":
      return Database;
    case "pdf":
    case "document":
    case "doc":
      return FileText;
    default:
      return File;
  }
}

function formatScore(score: number | null | undefined): string | null {
  if (score == null) return null;
  return (score * 100).toFixed(0) + "%";
}

export function SourceCard({ source, index }: SourceCardProps) {
  const Icon = getSourceIcon(source.source_type);
  const rerankerScore =
    "reranker_score" in source ? source.reranker_score : undefined;
  const score = "score" in source ? source.score : undefined;
  const displayScore = formatScore(rerankerScore ?? score);

  const fileName = source.source_path.split("/").pop() ?? source.source_path;

  return (
    <div className="flex items-start gap-2.5 p-2.5 rounded-lg border border-border-subtle bg-bg-surface hover:bg-bg-hover transition-colors group">
      <div className="flex-shrink-0 mt-0.5 w-6 h-6 rounded flex items-center justify-center bg-bg-elevated">
        <Icon size={12} className="text-text-muted" />
      </div>

      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-0.5">
          <span className="text-2xs font-mono text-text-muted">
            [{index + 1}]
          </span>
          <span className="text-xs font-medium text-text-primary truncate">
            {source.title}
          </span>
        </div>

        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-2xs text-text-muted truncate max-w-[180px]">
            {fileName}
          </span>
          <span className="text-2xs px-1.5 py-0.5 rounded bg-bg-elevated text-text-secondary border border-border-subtle">
            {source.source_type}
          </span>
          <span className="text-2xs px-1.5 py-0.5 rounded bg-bg-elevated text-text-secondary border border-border-subtle">
            {source.doc_type}
          </span>
          {displayScore && (
            <span className="text-2xs px-1.5 py-0.5 rounded bg-accent-dim text-accent border border-accent/20">
              {displayScore}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
