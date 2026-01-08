import { GitHubRepo, Project } from "@/types";

const GITHUB_USERNAME = "ashir6129";
const GITHUB_API_BASE = "https://api.github.com";

/**
 * Fetch all public repositories for the configured GitHub user.
 * Uses ISR (Incremental Static Regeneration) for automatic updates.
 */
export async function getGitHubRepos(): Promise<GitHubRepo[]> {
    try {
        const response = await fetch(
            `${GITHUB_API_BASE}/users/${GITHUB_USERNAME}/repos?sort=updated&per_page=100`,
            {
                headers: {
                    Accept: "application/vnd.github.v3+json",
                    // Add token for higher rate limits if available
                    ...(process.env.GITHUB_TOKEN && {
                        Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
                    }),
                },
                next: {
                    revalidate: 60, // Revalidate every minute for faster updates
                },
                cache: "no-store", // Force fresh fetch during development
            }
        );

        if (!response.ok) {
            console.error("GitHub API error:", response.status, response.statusText);
            // Return fallback data if API fails
            return getFallbackRepos();
        }

        const repos: GitHubRepo[] = await response.json();

        // Filter out forks
        return repos.filter((repo) => !repo.fork);
    } catch (error) {
        console.error("GitHub API fetch error:", error);
        return getFallbackRepos();
    }
}

/**
 * Fallback repos in case GitHub API fails (rate limiting)
 */
function getFallbackRepos(): GitHubRepo[] {
    return [
        {
            id: 1,
            name: "Mushroom-Classification-Identification-and-IoT-based-Cultivation",
            full_name: "ashir6129/Mushroom-Classification-Identification-and-IoT-based-Cultivation",
            description: "Flutter app with ML-powered mushroom identification and IoT integration for smart cultivation",
            html_url: "https://github.com/ashir6129/Mushroom-Classification-Identification-and-IoT-based-Cultivation",
            homepage: null,
            language: "Dart",
            stargazers_count: 5,
            forks_count: 1,
            watchers_count: 5,
            topics: ["flutter", "machine-learning", "iot", "pytorch"],
            created_at: "2024-01-01T00:00:00Z",
            updated_at: "2025-01-07T00:00:00Z",
            pushed_at: "2025-01-07T00:00:00Z",
        },
        {
            id: 2,
            name: "Accountifier",
            full_name: "ashir6129/Accountifier",
            description: "An accounting and finance management application",
            html_url: "https://github.com/ashir6129/Accountifier",
            homepage: null,
            language: "TypeScript",
            stargazers_count: 3,
            forks_count: 0,
            watchers_count: 3,
            topics: ["react", "typescript", "finance"],
            created_at: "2024-06-01T00:00:00Z",
            updated_at: "2024-12-01T00:00:00Z",
            pushed_at: "2024-12-01T00:00:00Z",
        },
        {
            id: 3,
            name: "Portfolio-Website",
            full_name: "ashir6129/Portfolio-Website",
            description: "Personal portfolio website built with Next.js and Tailwind CSS",
            html_url: "https://github.com/ashir6129/Portfolio-Website",
            homepage: "https://ashirkhan.dev",
            language: "TypeScript",
            stargazers_count: 2,
            forks_count: 0,
            watchers_count: 2,
            topics: ["nextjs", "tailwindcss", "portfolio"],
            created_at: "2025-01-01T00:00:00Z",
            updated_at: "2025-01-07T00:00:00Z",
            pushed_at: "2025-01-07T00:00:00Z",
        },
        {
            id: 4,
            name: "AI-Chat-Assistant",
            full_name: "ashir6129/AI-Chat-Assistant",
            description: "An AI-powered chat assistant using modern NLP techniques",
            html_url: "https://github.com/ashir6129/AI-Chat-Assistant",
            homepage: null,
            language: "Python",
            stargazers_count: 4,
            forks_count: 1,
            watchers_count: 4,
            topics: ["python", "ai", "nlp", "chatbot"],
            created_at: "2024-03-01T00:00:00Z",
            updated_at: "2024-11-01T00:00:00Z",
            pushed_at: "2024-11-01T00:00:00Z",
        },
        {
            id: 5,
            name: "E-Commerce-Platform",
            full_name: "ashir6129/E-Commerce-Platform",
            description: "Full-stack e-commerce platform with modern UI/UX",
            html_url: "https://github.com/ashir6129/E-Commerce-Platform",
            homepage: null,
            language: "JavaScript",
            stargazers_count: 6,
            forks_count: 2,
            watchers_count: 6,
            topics: ["react", "nodejs", "mongodb", "ecommerce"],
            created_at: "2024-02-01T00:00:00Z",
            updated_at: "2024-10-01T00:00:00Z",
            pushed_at: "2024-10-01T00:00:00Z",
        },
        {
            id: 6,
            name: "Real-Time-Chat-App",
            full_name: "ashir6129/Real-Time-Chat-App",
            description: "Real-time messaging application with WebSocket support",
            html_url: "https://github.com/ashir6129/Real-Time-Chat-App",
            homepage: null,
            language: "TypeScript",
            stargazers_count: 3,
            forks_count: 0,
            watchers_count: 3,
            topics: ["websocket", "react", "nodejs", "realtime"],
            created_at: "2024-04-01T00:00:00Z",
            updated_at: "2024-09-01T00:00:00Z",
            pushed_at: "2024-09-01T00:00:00Z",
        },
    ];
}

/**
 * Transform GitHub repos into Project format
 */
export function transformReposToProjects(repos: GitHubRepo[]): Project[] {
    return repos.map((repo) => ({
        id: repo.id,
        name: repo.name,
        slug: repo.name.toLowerCase().replace(/[^a-z0-9]+/g, "-"),
        description: repo.description,
        githubUrl: repo.html_url,
        liveUrl: repo.homepage || null,
        language: repo.language,
        stars: repo.stargazers_count,
        forks: repo.forks_count,
        topics: repo.topics || [],
        updatedAt: repo.updated_at,
    }));
}

/**
 * Get language color for display
 */
export function getLanguageColor(language: string | null): string {
    const colors: Record<string, string> = {
        TypeScript: "#3178c6",
        JavaScript: "#f1e05a",
        Python: "#3572A5",
        Dart: "#00B4AB",
        Java: "#b07219",
        "C++": "#f34b7d",
        C: "#555555",
        HTML: "#e34c26",
        CSS: "#563d7c",
        Rust: "#dea584",
        Go: "#00ADD8",
        Kotlin: "#A97BFF",
        Swift: "#F05138",
        Ruby: "#701516",
    };

    return colors[language || ""] || "#6e7681";
}

/**
 * Format relative time
 */
export function formatRelativeTime(dateString: string): string {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return "Today";
    if (diffDays === 1) return "Yesterday";
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;
    return `${Math.floor(diffDays / 365)} years ago`;
}
