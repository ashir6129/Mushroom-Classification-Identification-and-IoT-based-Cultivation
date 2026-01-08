import { Metadata } from "next";

export const metadata: Metadata = {
    title: "Skills | Muhammad Ashir Khan",
    description: "My technical skills and expertise in software development, including languages, frameworks, databases, and tools.",
};

const skillCategories = [
    {
        title: "Languages",
        icon: "💻",
        skills: [
            { name: "TypeScript", level: 90 },
            { name: "JavaScript", level: 90 },
            { name: "Dart", level: 85 },
            { name: "Python", level: 80 },
            { name: "Java", level: 70 },
            { name: "C++", level: 65 },
        ],
    },
    {
        title: "Frameworks & Libraries",
        icon: "🚀",
        skills: [
            { name: "React", level: 90 },
            { name: "Next.js", level: 85 },
            { name: "Flutter", level: 85 },
            { name: "Node.js", level: 75 },
            { name: "Express", level: 70 },
            { name: "FastAPI", level: 70 },
        ],
    },
    {
        title: "Databases",
        icon: "🗄️",
        skills: [
            { name: "PostgreSQL", level: 80 },
            { name: "MongoDB", level: 75 },
            { name: "Firebase", level: 75 },
            { name: "Supabase", level: 70 },
            { name: "SQLite", level: 70 },
        ],
    },
    {
        title: "AI / ML",
        icon: "🤖",
        skills: [
            { name: "PyTorch", level: 70 },
            { name: "TensorFlow", level: 60 },
            { name: "ONNX Runtime", level: 65 },
            { name: "Scikit-learn", level: 65 },
        ],
    },
    {
        title: "Tools & Platforms",
        icon: "🛠️",
        skills: [
            { name: "Git & GitHub", level: 90 },
            { name: "VS Code", level: 95 },
            { name: "Docker", level: 65 },
            { name: "Vercel", level: 85 },
            { name: "Linux", level: 75 },
            { name: "Figma", level: 60 },
        ],
    },
];

function SkillBar({ name, level }: { name: string; level: number }) {
    return (
        <div className="mb-4">
            <div className="flex justify-between items-center mb-1">
                <span className="text-sm text-[var(--text-primary)]">{name}</span>
                <span className="text-xs text-[var(--text-muted)]">{level}%</span>
            </div>
            <div className="h-2 bg-[var(--bg-tertiary)] rounded-full overflow-hidden">
                <div
                    className="h-full rounded-full"
                    style={{
                        width: `${level}%`,
                        background: `linear-gradient(90deg, var(--accent-primary) 0%, var(--accent-secondary) 100%)`,
                    }}
                />
            </div>
        </div>
    );
}

export default function SkillsPage() {
    return (
        <div className="pt-24 pb-16">
            <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="text-center mb-16">
                    <span className="badge mb-4">Technical Expertise</span>
                    <h1 className="heading-lg mb-4">Skills & Technologies</h1>
                    <p className="body-lg max-w-2xl mx-auto">
                        A comprehensive overview of my technical skillset across different domains of software development.
                    </p>
                </div>

                {/* Skills Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {skillCategories.map((category) => (
                        <div key={category.title} className="card">
                            <div className="flex items-center gap-3 mb-6">
                                <span className="text-2xl">{category.icon}</span>
                                <h2 className="heading-sm">{category.title}</h2>
                            </div>
                            <div>
                                {category.skills.map((skill) => (
                                    <SkillBar key={skill.name} name={skill.name} level={skill.level} />
                                ))}
                            </div>
                        </div>
                    ))}
                </div>

                {/* Additional Skills */}
                <div className="mt-16">
                    <h2 className="heading-md text-center mb-8">Other Skills</h2>
                    <div className="flex flex-wrap justify-center gap-3">
                        {[
                            "REST APIs",
                            "GraphQL",
                            "Tailwind CSS",
                            "Framer Motion",
                            "Responsive Design",
                            "Agile/Scrum",
                            "CI/CD",
                            "Unit Testing",
                            "Data Structures",
                            "Algorithms",
                            "System Design",
                            "Problem Solving",
                        ].map((skill) => (
                            <span
                                key={skill}
                                className="px-4 py-2 bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-full text-sm text-[var(--text-secondary)] hover:border-[var(--accent-primary)] transition-colors"
                            >
                                {skill}
                            </span>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
