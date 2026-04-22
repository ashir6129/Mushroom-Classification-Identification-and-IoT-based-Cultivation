import { Metadata } from "next";

export const metadata: Metadata = {
    title: "About | Muhammad Ashir Khan",
    description: "Learn about my journey in Computer Science at FAST NUCES, internship experience, and passion for software development.",
};

const educationData = [
    {
        year: "2022 - 2026",
        title: "BS Computer Science",
        institution: "FAST NUCES, Peshawar",
        description: "Pursuing a degree in Computer Science with focus on software engineering, AI, and data science.",
        subjects: ["OOP", "DSA", "Operating Systems", "Database Systems", "Computer Networks", "AI/ML", "DevOps"],
    },
];

const timelineData = [
    {
        year: "2025",
        title: "Final Year Project",
        description: "Building 'Mushroom Classification & IoT-based Cultivation' - a full-stack Flutter app with ML-powered mushroom identification and IoT integration for smart cultivation.",
        type: "project",
    },
    {
        year: "2024",
        title: "Software Development Internship",
        organisation: "SolutionAve",
        description: "Worked on real-world projects involving Flutter mobile development, backend APIs, and database management. Gained hands-on experience in agile methodologies and production-grade code.",
        tech: ["Flutter", "Dart", "REST APIs", "Firebase", "Git"],
        type: "internship",
    },
    {
        year: "2023",
        title: "Started Exploring Web Development",
        description: "Began learning React, Next.js, and modern frontend technologies. Built several personal projects to solidify understanding.",
        type: "learning",
    },
    {
        year: "2022",
        title: "Joined FAST NUCES",
        description: "Started my Computer Science journey at FAST National University. Learned fundamentals of programming, data structures, and algorithms.",
        type: "education",
    },
];

export default function AboutPage() {
    return (
        <div className="pt-24 pb-16">
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="text-center mb-16">
                    <span className="badge mb-4">About Me</span>
                    <h1 className="heading-lg mb-4">My Journey</h1>
                    <p className="body-lg max-w-2xl mx-auto">
                        A passionate software developer with a love for building elegant, performant applications.
                    </p>
                </div>

                {/* Introduction */}
                <section className="mb-16">
                    <div className="glass-card p-8">
                        <h2 className="heading-md mb-4">
                            Hi, I&apos;m <span className="gradient-text">Ashir</span> 👋
                        </h2>
                        <div className="space-y-4 body-md">
                            <p>
                                I&apos;m a <strong className="text-[var(--text-primary)]">BS Computer Science</strong> student at{" "}
                                <span className="text-[var(--accent-primary)]">FAST NUCES</span>, graduating in 2026.
                                My passion lies at the intersection of elegant code and beautiful user experiences.
                            </p>
                            <p>
                                I specialize in <strong className="text-[var(--text-primary)]">frontend development</strong> with React, Next.js, and Flutter,
                                but I also enjoy diving into backend systems, databases, and machine learning.
                            </p>
                            <p>
                                When I&apos;m not coding, you&apos;ll find me exploring new technologies, contributing to open source,
                                or working on side projects that solve real-world problems.
                            </p>
                        </div>
                    </div>
                </section>

                {/* Education */}
                <section className="mb-16">
                    <h2 className="heading-md mb-8">Education</h2>
                    {educationData.map((edu, index) => (
                        <div key={index} className="card mb-4">
                            <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4 mb-4">
                                <div>
                                    <h3 className="heading-sm">{edu.title}</h3>
                                    <p className="text-[var(--accent-primary)]">{edu.institution}</p>
                                </div>
                                <span className="badge badge-cyan">{edu.year}</span>
                            </div>
                            <p className="body-sm mb-4">{edu.description}</p>
                            <div className="flex flex-wrap gap-2">
                                {edu.subjects.map((subject) => (
                                    <span key={subject} className="px-2 py-1 text-xs bg-[var(--bg-tertiary)] rounded">
                                        {subject}
                                    </span>
                                ))}
                            </div>
                        </div>
                    ))}
                </section>

                {/* Timeline */}
                <section className="mb-16">
                    <h2 className="heading-md mb-8">My Timeline</h2>
                    <div className="relative">
                        {/* Timeline Line */}
                        <div className="absolute left-4 top-0 bottom-0 w-px bg-[var(--border-subtle)]" />

                        {/* Timeline Items */}
                        <div className="space-y-8">
                            {timelineData.map((item, index) => (
                                <div key={index} className="relative pl-12">
                                    {/* Timeline Dot */}
                                    <div
                                        className={`absolute left-2 top-1 w-5 h-5 rounded-full border-2 ${item.type === "internship"
                                                ? "bg-[var(--accent-green)] border-[var(--accent-green)]"
                                                : item.type === "project"
                                                    ? "bg-[var(--accent-primary)] border-[var(--accent-primary)]"
                                                    : "bg-[var(--bg-tertiary)] border-[var(--border-light)]"
                                            }`}
                                    />

                                    <div className="card">
                                        <div className="flex items-center gap-3 mb-2">
                                            <span className="badge text-xs">{item.year}</span>
                                            {item.type === "internship" && (
                                                <span className="badge badge-green text-xs">Internship</span>
                                            )}
                                        </div>
                                        <h3 className="heading-sm mb-1">{item.title}</h3>
                                        {item.organisation && (
                                            <p className="text-[var(--accent-primary)] text-sm mb-2">{item.organisation}</p>
                                        )}
                                        <p className="body-sm mb-3">{item.description}</p>
                                        {item.tech && (
                                            <div className="flex flex-wrap gap-2">
                                                {item.tech.map((t) => (
                                                    <span key={t} className="px-2 py-0.5 text-xs bg-[var(--bg-tertiary)] text-[var(--text-tertiary)] rounded">
                                                        {t}
                                                    </span>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </section>

                {/* Outside of Coding */}
                <section>
                    <h2 className="heading-md mb-8">Beyond the Code</h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="card text-center">
                            <div className="text-3xl mb-3">🎯</div>
                            <h3 className="heading-sm mb-2">Problem Solving</h3>
                            <p className="body-sm">Love tackling complex algorithmic challenges</p>
                        </div>
                        <div className="card text-center">
                            <div className="text-3xl mb-3">🌍</div>
                            <h3 className="heading-sm mb-2">Open Source</h3>
                            <p className="body-sm">Contributing to and learning from the community</p>
                        </div>
                        <div className="card text-center">
                            <div className="text-3xl mb-3">📚</div>
                            <h3 className="heading-sm mb-2">Continuous Learning</h3>
                            <p className="body-sm">Always exploring new technologies and frameworks</p>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    );
}
