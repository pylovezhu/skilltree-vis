import json
import collections
from typing import List, Dict, Tuple


class SimpleSkillAnalyzer:
    def __init__(self, skill_bank_path: str = "skill_bank.json"):
        with open(skill_bank_path, 'r', encoding='utf-8') as f:
            self.skill_data = json.load(f)
        self.all_skills = self.skill_data["all_skills"]
        self.categories = self.skill_data["categories"]
        self.skill_to_category = self._build_skill_category_map()

    def _build_skill_category_map(self) -> Dict[str, str]:
        skill_map = {}
        for category, skills in self.categories.items():
            for skill in skills:
                skill_map[skill] = category
        return skill_map

    def extract_skills(self, text: str) -> List[str]:
        found_skills = []
        text_lower = text.lower()
        for skill in self.all_skills:
            if skill.lower() in text_lower:
                if skill not in found_skills:
                    found_skills.append(skill)
        return found_skills

    def build_cooccurrence_matrix(self, jds: List[Dict]) -> Tuple[Dict[str, int], Dict[Tuple[str, str], int]]:
        skill_count = collections.defaultdict(int)
        cooccurrence = collections.defaultdict(int)

        for jd in jds:
            skills = self.extract_skills(jd["description"])
            for skill in skills:
                skill_count[skill] += 1
            for i in range(len(skills)):
                for j in range(i + 1, len(skills)):
                    pair = tuple(sorted([skills[i], skills[j]]))
                    cooccurrence[pair] += 1

        return dict(skill_count), dict(cooccurrence)

    def compute_simple_tfidf(self, jds: List[Dict], skill_count: Dict[str, int]) -> Dict[str, float]:
        total_docs = len(jds)
        tfidf = {}
        for skill, count in skill_count.items():
            tf = count / total_docs
            idf = 1.0
            tfidf[skill] = tf * idf * 10
        return tfidf

    def generate_graph_data(self, jds: List[Dict], min_cooccurrence: int = 1) -> Dict:
        skill_count, cooccurrence = self.build_cooccurrence_matrix(jds)
        tfidf_scores = self.compute_simple_tfidf(jds, skill_count)

        category_list = list(self.categories.keys())
        color_map = {
            "编程语言": "#377eb8",
            "Web框架": "#009688",
            "数据处理": "#130654",
            "容器部署": "#2496ed",
            "数据库": "#f29111",
            "其他工具": "#f05032"
        }

        nodes = []
        for skill, count in skill_count.items():
            category_name = self.skill_to_category.get(skill, "其他工具")
            category_index = category_list.index(category_name) if category_name in category_list else len(category_list) - 1
            tfidf = tfidf_scores.get(skill, 0)
            base_size = 30
            size = base_size + (count * 3) + (tfidf * 2)
            
            skill_detail = self.skill_data.get("skill_details", {}).get(skill, {})
            
            nodes.append({
                "id": skill,
                "name": skill,
                "symbolSize": min(max(size, 25), 60),
                "category": category_index,
                "count": count,
                "tfidf": round(tfidf, 4),
                "itemStyle": {"color": color_map.get(category_name, "#999")},
                "description": skill_detail.get("description", "暂无描述"),
                "difficulty": skill_detail.get("difficulty", "未知"),
                "learning_weeks": skill_detail.get("learning_weeks", 0),
                "resources": skill_detail.get("resources", [])
            })

        links = []
        for (skill1, skill2), count in cooccurrence.items():
            if count >= min_cooccurrence:
                links.append({
                    "source": skill1,
                    "target": skill2,
                    "value": count
                })

        return {
            "categories": [{"name": name} for name in category_list],
            "nodes": nodes,
            "links": links
        }

    def save_graph_data(self, graph_data: Dict, output_path: str = "graph_data.json"):
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, ensure_ascii=False, indent=2)
        print(f"图表数据已保存至: {output_path}")


def main():
    print("=" * 60)
    print("SkillTree Vis - 简化版技能树分析器 (无需依赖)")
    print("=" * 60)

    analyzer = SimpleSkillAnalyzer()

    with open("sample_jds.json", 'r', encoding='utf-8') as f:
        sample_jds = json.load(f)

    print(f"\n📊 正在分析 {len(sample_jds)} 条 JD 数据...")
    graph_data = analyzer.generate_graph_data(sample_jds)

    print(f"\n✅ 分析完成！")
    print(f"   - 发现技能节点: {len(graph_data['nodes'])} 个")
    print(f"   - 发现技能关联: {len(graph_data['links'])} 条")
    print(f"   - 技能分类: {len(graph_data['categories'])} 类")

    print("\n💾 正在保存结果...")
    analyzer.save_graph_data(graph_data, "graph_data.json")

    print("\n🎉 分析成功！刷新浏览器查看可视化效果！")


if __name__ == "__main__":
    main()
