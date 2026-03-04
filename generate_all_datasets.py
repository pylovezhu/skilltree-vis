import json
from simple_analyzer import SimpleSkillAnalyzer


def main():
    print("=" * 60)
    print("SkillTree Vis - 批量生成多数据集")
    print("=" * 60)

    analyzer = SimpleSkillAnalyzer()

    with open("datasets.json", 'r', encoding='utf-8') as f:
        datasets_config = json.load(f)

    for dataset in datasets_config["datasets"]:
        dataset_id = dataset["id"]
        dataset_name = dataset["name"]
        jds = dataset["jds"]

        print(f"\n📊 正在生成数据集: {dataset_name}...")
        graph_data = analyzer.generate_graph_data(jds)
        output_path = f"data_{dataset_id}.json"
        analyzer.save_graph_data(graph_data, output_path)
        print(f"   - 技能节点: {len(graph_data['nodes'])} 个")
        print(f"   - 关联关系: {len(graph_data['links'])} 条")

    print("\n" + "=" * 60)
    print("✅ 所有数据集生成完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
