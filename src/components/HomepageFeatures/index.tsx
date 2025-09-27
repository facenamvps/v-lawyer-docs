import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  icon: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'AI-Powered Analysis',
    icon: '🤖',
    description: (
      <>
        Extract key information from legal documents instantly. Identify parties,
        obligations, risks, and deadlines with advanced AI that understands legal context.
      </>
    ),
  },
  {
    title: 'Secure Authentication',
    icon: '🔐',
    description: (
      <>
        Enterprise-grade security with OAuth device flow for interactive use and
        API keys for automation. No passwords stored locally, automatic token refresh.
      </>
    ),
  },
  {
    title: 'Developer Friendly',
    icon: '⚡',
    description: (
      <>
        Built for developers and legal tech teams. Simple CLI commands, comprehensive
        REST API, and SDKs for popular languages. Integrate in minutes, not days.
      </>
    ),
  },
];

const AdditionalFeatures: FeatureItem[] = [
  {
    title: 'Case Law Search',
    icon: '🔍',
    description: (
      <>
        Search through extensive case law databases with semantic search.
        Find relevant precedents filtered by jurisdiction and date.
      </>
    ),
  },
  {
    title: 'Document Management',
    icon: '📄',
    description: (
      <>
        Upload, analyze, and manage legal documents programmatically.
        Support for PDF, DOCX, and plain text formats.
      </>
    ),
  },
  {
    title: 'Open Source',
    icon: '🌟',
    description: (
      <>
        Kanuni CLI is fully open source under MIT license. Contribute, customize,
        and build on top of V-Lawyer for your specific needs.
      </>
    ),
  },
];

function Feature({title, icon, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className={styles.featureCard}>
        <div className="text--center">
          <div className={styles.featureIcon}>{icon}</div>
        </div>
        <div className="text--center padding-horiz--md">
          <Heading as="h3">{title}</Heading>
          <p>{description}</p>
        </div>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <>
      <section className={styles.features}>
        <div className="container">
          <div className="text--center margin-bottom--xl">
            <Heading as="h2">Why Choose V-Lawyer?</Heading>
            <p className={styles.sectionSubtitle}>
              Professional-grade legal intelligence tools for developers and legal teams
            </p>
          </div>
          <div className="row">
            {FeatureList.map((props, idx) => (
              <Feature key={idx} {...props} />
            ))}
          </div>
        </div>
      </section>

      <section className={styles.additionalFeatures}>
        <div className="container">
          <div className="row">
            {AdditionalFeatures.map((props, idx) => (
              <Feature key={idx} {...props} />
            ))}
          </div>
        </div>
      </section>

      <section className={styles.cta}>
        <div className="container text--center">
          <Heading as="h2">Ready to Get Started?</Heading>
          <p className={styles.ctaSubtitle}>
            Access V-Lawyer via Kanuni CLI or REST API and start analyzing legal documents with AI
          </p>
          <div className={styles.ctaButtons}>
            <a
              className="button button--primary button--lg"
              href="/docs/cli/installation">
              Install Kanuni CLI
            </a>
            <a
              className="button button--outline button--primary button--lg"
              href="/docs/api/authentication/overview">
              Explore the API
            </a>
          </div>
        </div>
      </section>
    </>
  );
}