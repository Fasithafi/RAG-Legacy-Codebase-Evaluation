import ast
import os
from typing import List, Dict, Any

def extract_code_blocks(directory: str) -> List[Dict[str, Any]]:
    """
    Parses Python files in a directory and extracts functions and classes
    as distinct blocks of code for RAG indexing.
    """
    documents = []

    for root, _, files in os.walk(directory):
        for file in files:
            if not file.endswith(".py"):
                continue

            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()

            try:
                tree = ast.parse(source)
            except SyntaxError:
                print(f"Skipping {file_path} due to syntax error")
                continue

            # We want to extract top-level functions and classes
            # and also methods inside classes.
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    # Get the source code for this node
                    # ast.get_source_segment is available in Python 3.8+
                    start_line = node.lineno - 1
                    end_line = node.end_lineno
                    lines = source.splitlines()
                    code_block = "\n".join(lines[start_line:end_line])

                    # Determine parent class if this is a method
                    parent_class = None
                    # This is a simplified way to find the parent class
                    # In a production system, we'd track the traversal stack
                    for parent in ast.walk(tree):
                        if isinstance(parent, ast.ClassDef):
                            for child in parent.body:
                                if child == node:
                                    parent_class = parent.name
                                    break

                    doc_id = f"{file}_{node.name}_{start_line}"
                    documents.append({
                        "id": doc_id,
                        "content": code_block,
                        "metadata": {
                            "file": file,
                            "start_line": start_line + 1,
                            "end_line": end_line,
                            "name": node.name,
                            "type": "function" if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else "class",
                            "parent_class": parent_class
                        }
                    })

    return documents

if __name__ == "__main__":
    import json
    blocks = extract_code_blocks("dummy_codebase")
    print(f"Extracted {len(blocks)} code blocks.")
    # Save to file for inspection
    with open("extracted_blocks.json", "w") as f:
        json.dump(blocks, f, indent=2)
