import { EntityRepository, Repository } from 'typeorm';
import { Post } from '../entities/post.entity';
import { PostSection } from '../entities/post-section.entity';

@EntityRepository(Post)
export class PostRepository extends Repository<Post> {

  async findValidPosts(
    blogId: number,
    authorIds?: number[],
    sectionCode?: string,
    offset = 0,
    limit = 10,
    allowedStatuses?: string[],  // ex: ['검토중', '검토완료', '게시됨']
  ): Promise<Post[]> {
    const query = this.createQueryBuilder('post')
        .leftJoinAndSelect('post.postSections', 'section');

    // 조건 붙이기
    if (blogId) {
        query.andWhere('post.blogId = :blogId', { blogId: blogId });
    }

    if (authorIds && authorIds.length > 0) {
        query.andWhere('post.authorId IN (:...authorIds)', { authorIds: authorIds });
    }

    if (sectionCode) {
      const subQuery = query.subQuery()
        .select('section.postId')
        .from(PostSection, 'section')
        .where('section.sectionCode = :sectionCode', { sectionCode })
        .getQuery();

      if (offset > 0) {
        query.andWhere(`post.id NOT IN ${subQuery}`);
      } else {
        query.andWhere(`post.id IN ${subQuery}`);
      }
    }

    if (allowedStatuses && allowedStatuses.length > 0) {
      query.andWhere('section.permitComment = true')
           .andWhere('section.sectionStatus IN (:...allowedStatuses)', { allowedStatuses });
    }

    query.orderBy('post.postedAt', 'DESC')
         .skip(offset)
         .take(limit);

    return query.getMany();
  }
}