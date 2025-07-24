import { Injectable } from '@nestjs/common';
import { PostRepository } from '../repositories/post.repository';
import { Post } from '../entities/post.entity';

@Injectable()
export class PostService {
  constructor(private readonly postRepository: PostRepository) {}

  async getValidPosts(params: {
    blogId: number;
    authorIds?: number[];
    sectionCode?: string;
    offset?: number;
    editTiming?: '검토중' | '검토완료';
  }): Promise<Post[]> {
    const { blogId, authorIds, sectionCode, offset = 0, editTiming } = params;

    // 비즈니스 로직: editTiming에 따른 허용 상태 목록 결정
    const allowedStatuses = this.getAllowedStatuses(editTiming);

    // Repository 호출
    return this.postRepository.findValidPosts(
      blogId,
      authorIds,
      sectionCode,
      offset,
      10,  // page size 고정
      allowedStatuses,
    );
  }

  private getAllowedStatuses(editTiming?: string): string[] {
    switch (editTiming) {
      case '검토중':
        return ['검토중', '검토완료', '게시됨'];
      case '검토완료':
        return ['검토완료', '게시됨'];
      default:
        return [];
    }
  }
}