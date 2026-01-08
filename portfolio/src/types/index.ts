export interface GitHubRepo {
    id: number;
    name: string;
    full_name: string;
    description: string | null;
    html_url: string;
    homepage: string | null;
    language: string | null;
    stargazers_count: number;
    forks_count: number;
    watchers_count: number;
    topics: string[];
    created_at: string;
    updated_at: string;
    pushed_at: string;
    fork?: boolean;
}

export interface Project {
    // From GitHub
    id: number;
    name: string;
    slug: string;
    description: string | null;
    githubUrl: string;
    liveUrl: string | null;
    language: string | null;
    stars: number;
    forks: number;
    topics: string[];
    updatedAt: string;

    // From CMS (optional overrides)
    title?: string;
    customDescription?: string;
    images?: string[];
    featured?: boolean;
}

export interface SanityProject {
    _id: string;
    repoName: string;
    title?: string;
    description?: string;
    images?: {
        asset: {
            _ref: string;
            url?: string;
        };
    }[];
    featured?: boolean;
}
