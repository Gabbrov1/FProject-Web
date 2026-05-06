import { useState, type JSX } from "react";
import "../styles/browseTreeView.scss";

type TreeNode = {
  name: string;
  children: TreeNode[];
};

// Maps file extensions (and folders) to emoji icons
function getFileIcon(name: string, isFolder: boolean): string {
  if (isFolder) return "📁";
  const ext = name.split(".").pop();
  switch (ext) {
    case "tsx":
    case "ts":    return "🟦";
    case "astro": return "🚀";
    case "scss":
    case "css":   return "🎨";
    case "json":  return "📋";
    default:      return "📄";
  }
}

// Renders a single node and recursively renders its children if open
function TreeItem({ node, level }: { node: TreeNode; level: number }): JSX.Element {
    const isFolder = node.children.length > 0;
    const [open, setOpen] = useState(true);

    // Indentation grows with nesting level
    const INDENT_BASE_PX = 8;  
    const INDENT_PER_LEVEL_PX = 4;

    const indentPx = INDENT_BASE_PX + level * INDENT_PER_LEVEL_PX;

    return (
        <div>
            {/* Clickable row — folders toggle open/closed, files do nothing */}
            <div
            className={`tree-row ${isFolder ? "tree-row--folder" : "tree-row--file"}`}
            style={{ paddingLeft: `${indentPx}px` }}
            onClick={() => isFolder && setOpen((o) => !o)}
            >
            {/* Chevron for folders, blank spacer for files */}
            {isFolder
                ? <span className={`tree-chevron ${open ? "tree-chevron--open" : "tree-chevron--closed"}`}>▶</span>
                : <span className="tree-chevron-placeholder" />
            }

            <span className="tree-icon">{getFileIcon(node.name, isFolder)}</span>
            <span className={isFolder ? "tree-label--folder" : "tree-label--file"}>{node.name}</span>
            </div>

            {/* Children — only rendered when folder is open */}
            {isFolder && open && (
            <div className="tree-children" style={{ marginLeft: `${indentPx}px` }}>
                {node.children.map((child) => (
                <TreeItem key={child.name} node={child} level={level + 1} />
                ))}
            </div>
            )}
        </div>
        );
    }

export default function BrowseTreeView(): JSX.Element {
    const tree: TreeNode = {
        name: "root",
        children: [
            {
            name: "src",
            children: [
                {
                name: "components",
                children: [
                    { name: "navbar.astro", children: [] },
                    { name: "browseTreeView.tsx", children: [] },
                ],
                },
                {
                    name: "layouts",
                    children: [{ name: "Layout.astro", children: [] }],
                },
                {
                name: "pages",
                children: [
                    { name: "index.astro", children: [] },
                    { name: "browse.astro", children: [] },
                ],
                },
            ],
            },
            { 
                name: "public", children: [] 
            },
            {
                name: "styles",
                children: [{ name: "global.scss", children: [] }],
            },
        ],
    };

  return (
    <div>
      <h3>Browse:</h3>
      <div className="treeView">
        <TreeItem node={tree} level={0} />
      </div>
    </div>
  );
}