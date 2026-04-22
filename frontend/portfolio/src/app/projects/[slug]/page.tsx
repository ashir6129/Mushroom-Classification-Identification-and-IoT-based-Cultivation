import { Metadata } from "next";
import { notFound } from "next/navigation";
import { getGitHubRepos, transformReposToProjects, formatRelativeTime, getLanguageColor } from "@/lib/github";
import Link from "next/link";

interface PageProps {
    params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
    const { slug } = await params;
    const repos = await getGitHubRepos();
    const projects = transformReposToProjects(repos);
    const project = projects.find((p) => p.slug === slug);

    if (!project) {
        return { title: "Project Not Found" };
    }

    return {
        title: `${project.name} | Muhammad Ashir Khan`,
        description: project.description || `View the ${project.name} project`,
    };
}

export default async function ProjectDetailPage({ params }: PageProps) {
    const { slug } = await params;
    const repos = await getGitHubRepos();
    const projects = transformReposToProjects(repos);
    const project = projects.find((p) => p.slug === slug);

    if (!project) {
        notFound();
    }

    return (
        <div className="pt-24 pb-16">
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Back Button */}
                <Link
                    href="/projects"
                    className="inline-flex items-center gap-2 text-[var(--text-secondary)] hover:text-[var(--accent-primary)] transition-colors mb-8"
                >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                    </svg>
                    Back to Projects
                </Link>

                {/* Project Header */}
                <div className="mb-12">
                    <div className="flex items-start justify-between gap-4 flex-wrap mb-4">
                        <h1 className="heading-lg">{project.title || project.name}</h1>
                        <div className="flex items-center gap-3">
                            <a
                                href={project.githubUrl}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="btn-secondary py-2"
                            >
                                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                    <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                                </svg>
                                View on GitHub
                            </a>
                            {project.liveUrl && (
                                <a
                                    href={project.liveUrl}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="btn-primary py-2"
                                >
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                                    </svg>
                                    Live Demo
                                </a>
                            )}
                        </div>
                    </div>

                    <p className="body-lg mb-6">
                        {project.customDescription || project.description || "No description available."}
                    </p>

                    {/* Meta Information */}
                    <div className="flex flex-wrap items-center gap-6 text-sm">
                        {project.language && (
                            <div className="flex items-center gap-2">
                                <span
                                    className="w-3 h-3 rounded-full"
                                    style={{ backgroundColor: getLanguageColor(project.language) }}
                                />
                                <span className="text-[var(--text-secondary)]">{project.language}</span>
                            </div>
                        )}
                        <div className="flex items-center gap-1 text-[var(--text-secondary)]">
                            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                            </svg>
                            {project.stars} stars
                        </div>
                        <div className="flex items-center gap-1 text-[var(--text-secondary)]">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                            </svg>
                            {project.forks} forks
                        </div>
                        <span className="text-[var(--text-muted)]">
                            Updated {formatRelativeTime(project.updatedAt)}
                        </span>
                    </div>
                </div>

                {/* Topics */}
                {project.topics.length > 0 && (
                    <div className="mb-12">
                        <h2 className="heading-sm mb-4">Technologies</h2>
                        <div className="flex flex-wrap gap-2">
                            {project.topics.map((topic) => (
                                <span key={topic} className="badge">
                                    {topic}
                                </span>
                            ))}
                        </div>
                    </div>
                )}

                {/* Image Gallery Placeholder */}
                {project.images && project.images.length > 0 ? (
                    <div className="mb-12">
                        <h2 className="heading-sm mb-4">Gallery</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {project.images.map((image, index) => (
                                <div key={index} className="relative aspect-video rounded-xl overflow-hidden bg-[var(--bg-tertiary)]">
                                    <img src={image} alt={`${project.name} screenshot ${index + 1}`} className="w-full h-full object-cover" />
                                </div>
                            ))}
                        </div>
                    </div>
                ) : (
                    <div className="card text-center py-12 mb-12">
                        <div className="text-4xl mb-4">🖼️</div>
                        <h3 className="heading-sm mb-2">No images yet</h3>
                        <p className="body-sm">
                            Images for this project can be added via the CMS dashboard.
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
}
