---


cssclass: research-note
type: "{{itemType}}"
title: "{{title}}"
authors: "{% for creator in creators | filterby('creatorType', 'author') -%}{{creator.lastName}}, {{creator.firstName}}{% if not loop.last %}; {% endif %}{%- endfor %}"
publication: "{{publicationTitle}}"
date: {{date | format("YYYY-MM-DD")}}
lastmod: 2025-11-26
citekey: {{citekey}}
doi: "{{DOI}}"
url: "{{uri}}"
pdf: {% for attachment in attachments | filterby("path","endswith",".pdf") %}file://{{attachment.path | replace(" ", "%20")}}{% if not loop.last %}, {% endif %}{% endfor %}
tags:
- Ubuntu
- Zotero
---

## 📘 Reference Information
**Title:** {{title}}  
**Authors:** {% for creator in creators | filterby("creatorType","author") -%}{{creator.lastName}}, {{creator.firstName}}{% if not loop.last %}; {% endif %}{%- endfor %}  
**Publication:** {{publicationTitle}} ({{date | format("YYYY")}})  
**Citekey:** `{{citekey}}`  
**DOI:** {% if DOI %}[{{DOI}}](https://doi.org/{{DOI}}){% else %}-{% endif %}  
**Links:** [Online]({{uri}}){% for attachment in attachments | filterby("path","endswith",".pdf") %} | [PDF](file://{{attachment.path | replace(" ", "%20")}}){% endfor %}

---

## 🧾 Metadata
- **Start date:** {% if date %}{{date | format("YYYY-MM-DD")}}{% endif %}
- **End date:** 
- **Page range:** {% for annotation in annotations %}{% if loop.first %}{{annotation.pageLabel}}{% endif %}{% endfor %}
- **Keywords:** {% for t in tags %}#{{t.tag | lower | replace(" ", "-")}} {% endfor %}

---

## 🧠 Abstract / Summary
> 简要概述研究的背景、目标、方法、结果与结论（建议 3–5 句）。

---

## 🔍 Key Concepts
| 核心概念 | 说明 |
|-----------|------|
| **Problem** | |
| **Method / Model** | |
| **Result** | |
| **Contribution** | |

---

## 💬 Highlights & Annotations
{% macro calloutHeader(color) -%}
{%- if color == "#ffd400" -%}📌 Important{%- endif -%}
{%- if color == "#5fb236" -%}📗 Reference{%- endif -%}
{%- if color == "#2ea8e5" -%}💡 Insight{%- endif -%}
{%- if color == "#a28ae5" -%}🔧 Method{%- endif -%}
{%- if color == "#ff6666" -%}⚠️ Critique{%- endif -%}
{%- endmacro -%}

{% persist "annotations" %}
{% set annotations = annotations | filterby("date", "dateafter", lastImportDate) -%}
{% if annotations.length > 0 %}
### Imported on {{importDate | format("YYYY-MM-DD h:mm a")}}

{%- for annotation in annotations %}
>[!quote{% if annotation.color %}|{{annotation.color}}{% endif %}]+ **{{calloutHeader(annotation.color)}}**
> {{annotation.annotatedText}}  
> [(p. {{annotation.pageLabel}})](zotero://open-pdf/library/items/{{annotation.attachment.itemKey}}?page={{annotation.pageLabel}}&annotation={{annotation.id}})

{% if annotation.comment%}
> 💭 *{{annotation.comment}}*
{% endif %}
{% if annotation.imageRelativePath %}
![](/obsidian/Zotero/template/%7B%7Bannotation.imageRelativePath%7D%7D)
{% endif %}
---
{%- endfor %}{% endif %} {% endpersist %}

---

## 🧩 Reflections / Insights
- 这篇文献的核心创新是什么？  
- 与已有研究相比，它的主要改进点在哪？  
- 可能的局限性或未来方向？  

---

## 🔗 Connections
- **Related Works:**  
  - 
- **Relevance to My Research:**  
  - 

---

## 🧾 Citation
> {{bibliography}}
